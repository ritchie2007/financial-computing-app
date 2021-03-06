1 # pylint: disable=no-member

from random import random
import os, copy
import time
from time import strftime, localtime
from datetime import timedelta, datetime #, date
from pytz import timezone
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_parse
from sqlalchemy import desc, asc, func, or_ 

from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, request, url_for, session, make_response, json
from flask import send_from_directory, send_file, after_this_request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, WebNavForm
from app.models import User, Data_table, activity_code, CorporationReport, Staff, Task, Timesheet, Corporation, Individual, Job_type, Userlog, Mulform, TimesheetTempData
#from app import dateCalculate
from app import utility
from app.utility import userrecrods, authentication, get_corp_name
# from tkinter import messagebox
# from tkinter import *

@app.before_request
def before_request():
    ''' is_authenticated'''
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    else:
        pass

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    form = WebNavForm()

    if form.validate_on_submit():
        link = form.website.data
        if link is not None:
            if link.find("http://") != 0 and link.find("https://") != 0:
                link = "http://" + link
            return redirect(link)
    else:
        return render_template(
            'index.html',
            title='Home',
            form=form
        )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            typein = form.username.data
            print('typein: ', typein)
            authenticated = authentication(typein)
            if authenticated:
                user = User.query.filter_by(username=typein).first()
                print('after authenticated, user: ', user)
                if user is None:
                    print('---- user is none ----')
                    flash('Invalid username or password')
                    userrecrods(typein, 'username')
                    return redirect(url_for('login'))
                elif user.check_password(form.password.data) is False:
                    print('---- password wrong ----')
                    flash('Invalid username or password')
                    userrecrods(typein, 'password')
                    return redirect(url_for('login'))
                else:
                    login_user(user, remember=form.remember_me.data)
                    next_page = request.args.get('next')
                    if not next_page or url_parse(next_page).netloc != '':
                        userrecrods(typein, '')
                        return redirect(url_for('index'))
                    else:
                        return redirect(next_page)
            else:
                # This code is to hide the main tkinter window
                print('authentication: ', authenticated)
                userrecrods(typein, 'lock')
                flash('You are redirected to Homepage as you attmepted "Login" too many times! \n (if attmepts > 3 times, you have to try one hour later; \n if attempts > 6 times, you have to try 24 hours later.)')
                return redirect(url_for('index'))
                # root = Tk()
                # root.title('Login error')
                # root.attributes("-topmost", True)
                # w = 400     # popup window width
                # h = 200     # popup window height
                # sw = root.winfo_screenwidth()
                # sh = root.winfo_screenheight()
                # x = (sw - w)/2
                # y = (sh - h)/2
                # root.geometry('%dx%d+%d+%d' % (w, h, x, y))
                # m = 'Attmepted Login too many times! \n if attmepts > 3 times, you have to try one hour later; \n if attempts > 6 times, you have to try 24 hours later.'
                # w = Label(root, text=m, width=120, height=10)
                # w.pack()
                # b = Button(root, text="OK", command=root.destroy, width=10)
                # b.pack()
                # mainloop()
                # return redirect(url_for('index'))
        else:
            return render_template(
                'login.html',
                title = 'Login',
                form = form
            )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    else:
        form = RegistrationForm()

        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, identification=int(time.time())+31536000)
            user.set_password(form.password.data)
            print(type(user), user.password_hash)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you have registered successfully!')
            return redirect(url_for('login'))

        else:
            return render_template(
                'register.html',
                title='Register',
                form=form
            )

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template(
        'profile.html',
        user=user
    )

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        user = User.query.filter_by(username=current_user.username).first()
        flash('Saved username: {}'.format(user.username))
        flash('Saved user description: {}'.format(user.about_me))
        return redirect(url_for('profile', username=current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
   
    else:
        pass

    return render_template(
        'edit_profile.html',
        title='Edit profile',
        form=form
    )

@app.route('/corporate')
@login_required
def corporate():
    corp = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp1, Corporation.corp2, Corporation.corp8, Corporation.corp9, Corporation.corp10, Corporation.corp25, Corporation.corp18, Corporation.corp19, Corporation.corp20, Corporation.task).order_by(Corporation.corp2)
    return render_template(
        'corp.html',
        corp = corp,
        title='Corporate'
    )

@app.route('/corp_add', methods=['GET', 'POST'])
@login_required
def corp_add():
    indivlist = Individual.query.with_entities(Individual.indiv_id, Individual.sin, Individual.prefix, Individual.last_name, Individual.first_name, Individual.address1, Individual.phone1, Individual.email, Individual.wechat)
    corplist = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp1, Corporation.corp2)
    max_id = db.session.query(func.max(Corporation.corp_id)).scalar()

    if request.method == 'POST':
        corp1 = request.form['corp1']
        corp2 = request.form['corp2']
        corp3 = request.form['corp3']
        corp4 = request.form['corp4']
        corp5 = request.form['corp5']
        corp6 = request.form['corp6']
        corp7 = request.form['corp7']
        corp8 = request.form['corp8']
        corp9 = request.form['corp9']
        corp10 = request.form['corp10']
        corp11 = request.form['corp11']
        corp12 = request.form['corp12']
        corp13 = request.form['corp13']
        corp14 = request.form['corp14']
        corp15 = request.form['corp15']
        corp16 = request.form['corp16']
        corp17 = request.form['corp17']
        corp18 = request.form['corp18']
        corp19 = request.form['corp19']
        corp20 = request.form['corp20']
        corp21 = request.form['corp21']
        corp22 = request.form['corp22']
        corp23 = request.form['corp23']
        corp24 = request.form['corp24']
        corp25 = request.form['corp25']
        corp26 = request.form['corp26']
        corp27 = request.form['corp27']
        corp28 = request.form['corp28']
        corp29 = request.form['corp29']
        corp30 = request.form['corp30']
        corp31 = request.form['corp31']
        corp32 = request.form['corp32']
        corp33 = request.form['corp33']
        corp34 = request.form['corp34']
        corp35 = request.form['corp35']
        corp36 = request.form['corp36']
        corp37 = request.form['corp37']
        corp38 = request.form['corp38']
        corp39 = request.form['corp39']
        corp40 = request.form['corp40']
        corp41 = request.form['corp41']
        corp42 = request.form['corp42']
        corp43 = request.form['corp43']
        corp44 = request.form['corp44']
        corp45 = request.form['corp45']
        corp46 = request.form['corp46']
        corp47 = request.form['corp47']
        corp48 = request.form['corp48']
        corp49 = request.form['corp49']
        corp50 = request.form['corp50']
        corp51 = request.form['corp51']
        corp52 = request.form['corp52']
        corp53 = request.form['corp53']
        corp54 = request.form['corp54']
        corp55 = request.form['corp55']
        corp56 = request.form['corp56']
        corp57 = request.form['corp57']
        corp58 = request.form['corp58']

        corp201 = corp20.replace('-','')
        corp211 = corp21.replace('-','')

        task = 0
        recent_update = ""
        timemark = datetime.utcnow()
        contact_position = ""
        contact_position += ((request.form['corp'+str(59)])+','+(request.form['corp'+str(61)])+',')
        contact_position += ((request.form['corp'+str(63)])+','+(request.form['corp'+str(65)]))

        shareholder_info = ""
        shareholder_info += (request.form['corp'+str(71)]+','+request.form['corp'+str(72)]+',')
        shareholder_info += (request.form['corp'+str(74)]+','+request.form['corp'+str(75)]+',')
        shareholder_info += (request.form['corp'+str(77)]+','+request.form['corp'+str(78)]+',')
        shareholder_info += (request.form['corp'+str(80)]+','+request.form['corp'+str(81)])

        shareholder_corp_info = ""
        shareholder_corp_info += (request.form['corp'+str(83)]+','+request.form['corp'+str(84)]+',')
        shareholder_corp_info += (request.form['corp'+str(86)]+','+request.form['corp'+str(87)]+',')
        shareholder_corp_info += (request.form['corp'+str(89)]+','+request.form['corp'+str(90)]+',')
        shareholder_corp_info += (request.form['corp'+str(92)]+','+request.form['corp'+str(93)])

        corp_as_shareholder = ""

        name = []
        for x in [60, 62, 64, 66, 67, 68, 69, 70, 73, 76, 79, 82, 85, 88, 91, 94, 95, 96, 97, 98]:
            a = (request.form['corp' + str(x)])
            name.append(request.form['corp' + str(x)])
        contact = utility.get_id_from_name(name, 0, 4)
        director = utility.get_id_from_name(name, 4, 4)
        shareholder = utility.get_id_from_name(name, 8, 4)
        shareholder_corp = utility.get_id_from_name(name, 12, 4)
        # corp_as_shareholder = utility.get_id_from_name(name, 16, 4)
        corp_as_shareholder = ''

        if (max_id == None):
            max_id = 1
        else:
            max_id = max_id + 1
        
        if contact == []:
            contact = ""
        else:
            utility.corp_contact_to_indiv(contact, max_id, 0, "")
            contact = ",".join(contact)
        if director == []:
            director = ""
        else:
            utility.corp_director_to_indiv(director, max_id, 0, "")
            director = ",".join(director)
        if shareholder == []:
            shareholder = ""
        else:
            utility.corp_shareholder_to_indiv(shareholder, max_id, 0, "")
            shareholder = ",".join(shareholder)
  
        if shareholder_corp == []:
            shareholder_corp = ""
        else:
            utility.corp_shareholder_to_corp(shareholder_corp, max_id, 0, "")
            shareholder_corp = ",".join(shareholder_corp)

        my_data = Corporation(corp1, corp2, corp3, corp4, corp5, corp6, corp7, corp8, corp9, corp10, corp11, corp12, corp13, corp14, corp15, corp16, corp17, corp18, corp19, corp20, corp21, corp201, corp211, corp22, corp23, corp24, corp25, corp26, corp27, corp28, corp29, corp30, corp31, corp32, corp33, corp34, corp35, corp36, corp37, corp38, corp39, corp40, corp41, corp42, corp43, corp44, corp45, corp46, corp47, corp48, corp49, corp50, corp51, corp52, corp53, corp54, corp55, corp56, corp57, corp58, contact, director, shareholder, task, recent_update, contact_position, shareholder_info, shareholder_corp, shareholder_corp_info, corp_as_shareholder, timemark)
        db.session.add(my_data)
        db.session.commit()
        flash("A Corporation Added Successfully")
        return redirect(url_for('corporate'))
        
    return render_template(
        'corp_add.html',
        indiv_data = indivlist,
        corp_data = corplist,
        title='Add_new_Corporation'
    )

@app.route('/corp_edit', methods=['GET', 'POST'])
@app.route('/corp_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def corp_edit(id):
    my_data = Corporation.query.get(id)
    indiv_data = Individual.query.with_entities(Individual.indiv_id, Individual.sin, Individual.prefix, Individual.last_name, Individual.first_name, Individual.phone1, Individual.wechat, Individual.email)
    corps = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp1, Corporation.corp2)
    value0 = []
    value0.append(my_data.contact)
    value0.append(my_data.director)
    value0.append(my_data.shareholder)
    indiv_list = utility.get_index_index('Corporation', value0, indiv_data)
    value0_corp = []
    value0_corp.append(my_data.shareholder_corp)
    corp_list = utility.get_index_index('Individual', value0_corp, corps)
    corp_as_shareholder = my_data.corp_as_shareholder
    corp_as_shareholder_list = []
    if corp_as_shareholder:
        if len(corp_as_shareholder)>0:
            corp_as_shareholder = corp_as_shareholder.split(',')
            for x in corp_as_shareholder:
                da = Corporation.query.get(int(x))
                corp_as_shareholder_list.append(str(da.corp_id)+' | '+str(da.corp1)+' | '+str(da.corp2))
    for x in range(len(corp_as_shareholder_list), 4):
        corp_as_shareholder_list.append("")
    print('as as: ', corp_as_shareholder_list)
    if request.method == 'POST':
        my_data.corp1 = request.form['corp1']
        my_data.corp2 = request.form['corp2']
        my_data.corp3 = request.form['corp3']
        my_data.corp4 = request.form['corp4']
        my_data.corp5 = request.form['corp5']
        my_data.corp6 = request.form['corp6']
        my_data.corp7 = request.form['corp7']
        my_data.corp8 = request.form['corp8']
        my_data.corp9 = request.form['corp9']
        my_data.corp10 = request.form['corp10']
        my_data.corp11 = request.form['corp11']
        my_data.corp12 = request.form['corp12']
        my_data.corp13 = request.form['corp13']
        my_data.corp14 = request.form['corp14']
        my_data.corp15 = request.form['corp15']
        my_data.corp16 = request.form['corp16']
        my_data.corp17 = request.form['corp17']
        my_data.corp18 = request.form['corp18']
        my_data.corp19 = request.form['corp19']
        my_data.corp20 = request.form['corp20']
        my_data.corp21 = request.form['corp21']
        my_data.corp22 = request.form['corp22']
        my_data.corp23 = request.form['corp23']
        my_data.corp24 = request.form['corp24']
        my_data.corp25 = request.form['corp25']
        my_data.corp26 = request.form['corp26']
        my_data.corp27 = request.form['corp27']
        my_data.corp28 = request.form['corp28']
        my_data.corp29 = request.form['corp29']
        my_data.corp30 = request.form['corp30']
        my_data.corp31 = request.form['corp31']
        my_data.corp32 = request.form['corp32']
        my_data.corp33 = request.form['corp33']
        my_data.corp34 = request.form['corp34']
        my_data.corp35 = request.form['corp35']
        my_data.corp36 = request.form['corp36']
        my_data.corp37 = request.form['corp37']
        my_data.corp38 = request.form['corp38']
        my_data.corp39 = request.form['corp39']
        my_data.corp40 = request.form['corp40']
        my_data.corp41 = request.form['corp41']
        my_data.corp42 = request.form['corp42']
        my_data.corp43 = request.form['corp43']
        my_data.corp44 = request.form['corp44']
        my_data.corp45 = request.form['corp45']
        my_data.corp46 = request.form['corp46']
        my_data.corp47 = request.form['corp47']
        my_data.corp48 = request.form['corp48']
        my_data.corp49 = request.form['corp49']
        my_data.corp50 = request.form['corp50']
        my_data.corp51 = request.form['corp51']
        my_data.corp52 = request.form['corp52']
        my_data.corp53 = request.form['corp53']
        my_data.corp54 = request.form['corp54']
        my_data.corp55 = request.form['corp55']
        my_data.corp56 = request.form['corp56']
        my_data.corp57 = request.form['corp57']
        my_data.corp58 = request.form['corp58']
        
        my_data.corp201 = (request.form['corp20']).replace('-','')
        my_data.corp211 = (request.form['corp21']).replace('-','')

        my_data.task = 0
        my_data.recent_update = ""
        my_data.timemark = datetime.utcnow()
        contact_position = ""
        contact_position += ((request.form['corp'+str(59)])+','+(request.form['corp'+str(61)])+',')
        contact_position += ((request.form['corp'+str(63)])+','+(request.form['corp'+str(65)]))
        shareholder_info = ""
        shareholder_info += (request.form['corp'+str(71)]+','+request.form['corp'+str(72)]+',')
        shareholder_info += (request.form['corp'+str(74)]+','+request.form['corp'+str(75)]+',')
        shareholder_info += (request.form['corp'+str(77)]+','+request.form['corp'+str(78)]+',')
        shareholder_info += (request.form['corp'+str(80)]+','+request.form['corp'+str(81)])
        shareholder_corp_info = ""
        shareholder_corp_info += (request.form['corp'+str(83)]+','+request.form['corp'+str(84)]+',')
        shareholder_corp_info += (request.form['corp'+str(86)]+','+request.form['corp'+str(87)]+',')
        shareholder_corp_info += (request.form['corp'+str(89)]+','+request.form['corp'+str(90)]+',')
        shareholder_corp_info += (request.form['corp'+str(92)]+','+request.form['corp'+str(93)])
        my_data.contact_position = contact_position
        my_data.shareholder_info = shareholder_info
        my_data.shareholder_corp_info = shareholder_corp_info
        #my_data.corp_as_shareholder

        name = []
        for x in [60, 62, 64, 66, 67, 68, 69, 70, 73, 76, 79, 82, 85, 88, 91, 94, 95, 96, 97, 98]:
            a = (request.form['corp' + str(x)])
            name.append(request.form['corp' + str(x)])
        contact = utility.get_id_from_name(name, 0, 4)
        director = utility.get_id_from_name(name, 4, 4)
        shareholder = utility.get_id_from_name(name, 8, 4)
        shareholder_corp = utility.get_id_from_name(name, 12, 4)
        # corp_as_shareholder = utility.get_id_from_name(name, 16, 4)
       
        max_id = id
        print("-- new contact id array --", contact, director, shareholder)


        if contact == []:
            my_data.contact = ""
        else:
            utility.corp_contact_to_indiv(contact, max_id, 1, value0[0])
            my_data.contact = ",".join(contact)

        if director == []:
            my_data.director = ""
        else:
            utility.corp_director_to_indiv(director, max_id, 1, value0[1])
            my_data.director = ",".join(director)

        if shareholder == []:
            my_data.shareholder = ""
        else:
            utility.corp_shareholder_to_indiv(shareholder, max_id, 1, value0[2])
            my_data.shareholder = ",".join(shareholder)

        if shareholder_corp == []:
            my_data.shareholder_corp = ""
        else:
            utility.corp_shareholder_to_corp(shareholder_corp, max_id, 1, value0_corp[0])
            my_data.shareholder_corp = ",".join(shareholder_corp)

        db.session.commit()
        flash("Corporation Updated Successfully")
        return redirect(url_for('corporate'))

    return render_template(
        'corp_edit.html',
        corp = my_data,
        indiv_data = indiv_data,
        corp_data = corps,
        indiv_list = indiv_list,
        corp_list = corp_list,
        as_shareholder = corp_as_shareholder_list,
        title='Edit_Corporation'
    )

@app.route('/corp_del', methods=['GET', 'POST'])
@app.route('/corp_del/<int:id>', methods=['GET', 'POST'])
def corp_del(id):
    my_data = Corporation.query.get(id)
    print(my_data)
    if request.method == 'POST':

        if my_data.contact:
            if len(my_data.contact) > 0:
                utility.corp_contact_to_indiv('', id, 2, my_data.contact)

        if my_data.director:
            if len(my_data.director) > 0:
                utility.corp_director_to_indiv('', id, 2, my_data.director)

        if my_data.shareholder:
            if len(my_data.shareholder) > 0:
                utility.corp_shareholder_to_indiv('', id, 2, my_data.shareholder)

        if my_data.shareholder_corp:
            if my_data.shareholder_corp != '(null)':
                print('shareholder_corp : ', my_data.shareholder_corp, id, len(my_data.shareholder_corp))
                if len(my_data.shareholder_corp) > 0:
                    utility.corp_shareholder_to_corp('', id, 2, my_data.shareholder_corp)

        if my_data.corp_as_shareholder:
            if my_data.corp_as_shareholder != '(null)':
                print('corp_as_shareholder : ', my_data.corp_as_shareholder, id)
                if len(my_data.corp_as_shareholder) > 0:
                    utility.corp_to_corp_shareholder('', id, 2, my_data.corp_as_shareholder)

        db.session.delete(my_data)
        db.session.commit()
        flash("Corporation Deleted Successfully")
        return redirect(url_for('corporate'))

    return render_template(
        'corp_edit.html',
        corp = my_data,
        title='Edit_Corporation')

@app.route('/individual')
@login_required
def individual():
    my_data = Individual.query.all()
    num = random()
    print(num)
    return render_template(
        'individual.html',
        indiv = my_data,
        title='Individual'
    )

@app.route('/individual_add', methods=['GET', 'POST'])
@login_required
def individual_add():
    corp = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp1, Corporation.corp2)
    indiv = Individual.query.with_entities(Individual.indiv_id, Individual.sin, Individual.prefix, Individual.last_name, Individual.first_name)
    max_id = db.session.query(func.max(Individual.indiv_id)).scalar()    
    if request.method == 'POST':
        sin = request.form['indiv1']
        prefix = request.form['indiv2']
        last_name = request.form['indiv3']
        first_name = request.form['indiv4']
        citizenship = request.form['indiv5']
        citizenship = 'PR' if citizenship.lower() == 'p' else citizenship
        citizenship = 'Citizen' if citizenship.lower() == 'c' else citizenship
        email = request.form['indiv6']
        phone1 = request.form['indiv7']
        phone2 = request.form['indiv8']
        phone1digit = phone1.replace('-','')
        phone2digit = phone2.replace('-','')
        address1 = request.form['indiv9']
        taxresident = request.form['indiv10']
        taxresident = 'Yes' if taxresident.lower() == 'y' else taxresident
        taxresident = 'No' if taxresident.lower() == 'n' else taxresident
        identity = request.form['indiv11']
        wechat = request.form['indiv12']
        cra_sole_proprietor = request.form['indiv13']
        cra_hst_report = request.form['indiv14']
        cra_payroll = request.form['indiv15']
        cra_withhold_tax = request.form['indiv16']
        cra_wsib = request.form['indiv17']
        cra_other = request.form['indiv18']
        oversea_asset_t1135 = request.form['indiv19']
        oversea_corp_t1134 = request.form['indiv20']
        tslip = request.form['indiv21']
        tax_personal_info = request.form['indiv22']
        specific_info = request.form['indiv23']
        engage_account = request.form['indiv24']
        engage_leading = request.form['indiv25']
        note = request.form['indiv26']
        name = []
        for x in range(19):
            name.append(request.form['indiv' + str(x+27)])
        contact_corp = utility.get_id_from_name(name, 0, 3)
        director_corp = utility.get_id_from_name(name, 3, 3)
        sharehold_corp = utility.get_id_from_name(name, 6, 3)
        spouse = utility.get_id_from_name(name, 9, 2)
        parent = utility.get_id_from_name(name, 11, 4)
        child = utility.get_id_from_name(name, 15, 4)
        timemark = datetime.utcnow()
        if (max_id == None):
            max_id = 1
        else:
            max_id = max_id + 1

        if contact_corp == []:
            contact_corp = ""
        else:
            utility.indiv_to_corp_contact(contact_corp, max_id, 0, "")
            contact_corp = ",".join(contact_corp)

        if director_corp == []:
            director_corp = ""
        else:
            utility.indiv_to_corp_director(director_corp, max_id, 0, "")
            director_corp = ",".join(director_corp)

        if sharehold_corp == []:
            sharehold_corp = ""
        else:
            utility.indiv_to_corp_shareholder(sharehold_corp, max_id, 0, "")
            sharehold_corp = ",".join(sharehold_corp)
        

        if spouse == []:
            spouse = ""
        else:
            utility.indiv_to_spouse(spouse, max_id, 0, "")
            spouse = ",".join(spouse)

        if parent == []:
            parent = ""
        else:
            utility.parent_to_child(parent, max_id, 0, "")
            parent = ",".join(parent)

        if child == []:
            child = ""
        else:
            utility.child_to_parent(child, max_id, 0, "")
            child = ",".join(child)
        
        my_data = Individual(sin, prefix, last_name, first_name, citizenship, email, phone1, phone2, phone1digit, phone2digit, address1, taxresident, identity, wechat, cra_sole_proprietor, cra_hst_report, cra_payroll, cra_withhold_tax, cra_wsib, cra_other, oversea_asset_t1135, 
        oversea_corp_t1134, tslip, tax_personal_info, specific_info, engage_account, engage_leading, note, contact_corp, director_corp, sharehold_corp, spouse, parent, child, timemark)
        db.session.add(my_data)
        db.session.commit()
        flash("Individual add Successfully")
        return redirect(url_for('individual'))

    return render_template(
        'individual_add.html', 
        title='Add_new_Individual',
        corp_data = corp,
        indiv_data = indiv
    )

@app.route('/individual_edit', methods=['GET', 'POST'])
@app.route('/individual_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def individual_edit(id):
    my_data = Individual.query.get(id)
    corp_dropdown = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp2, Corporation.corp1)
    indiv_dropdown = Individual.query.with_entities(Individual.indiv_id, Individual.sin, Individual.prefix, Individual.last_name, Individual.first_name)
    
    value0_corp = []
    value0_corp.append(my_data.contact_corp)
    value0_corp.append(my_data.director_corp)
    value0_corp.append(my_data.sharehold_corp)
    corp_list = utility.get_index_index('Individual', value0_corp, corp_dropdown)
    
    value0_indiv = []
    value0_indiv.append(my_data.spouse)
    value0_indiv.append(my_data.parent)
    value0_indiv.append(my_data.child)
    indiv_relation_list = utility.get_index_index('Corporation', value0_indiv, indiv_dropdown)

    if request.method == 'POST':
        my_data.sin = request.form['indiv1']
        my_data.prefix = request.form['indiv2']
        my_data.last_name = request.form['indiv3']
        my_data.first_name = request.form['indiv4']
        citizenship = request.form['indiv5']
        my_data.citizenship = 'PR' if citizenship.lower() == 'p' else citizenship
        my_data.citizenship = 'Citizen' if citizenship.lower() == 'c' else citizenship
        my_data.email = request.form['indiv6']
        my_data.phone1 = request.form['indiv7']
        my_data.phone2 = request.form['indiv8']
        my_data.address1 = request.form['indiv9']
        taxresident = request.form['indiv10']
        my_data.taxresident = 'Yes' if taxresident.lower() == 'y' else taxresident
        my_data.taxresident = 'No' if taxresident.lower() == 'n' else taxresident
        my_data.identity = request.form['indiv11']
        my_data.wechat = request.form['indiv12']
        my_data.cra_sole_proprietor = request.form['indiv13']
        my_data.cra_hst_report = request.form['indiv14']
        my_data.cra_payroll = request.form['indiv15']
        my_data.cra_withhold_tax = request.form['indiv16']
        my_data.cra_wsib = request.form['indiv17']
        my_data.cra_other = request.form['indiv18']
        my_data.oversea_asset_t1135 = request.form['indiv19']
        my_data.oversea_corp_t1134 = request.form['indiv20']
        my_data.tslip = request.form['indiv21']
        my_data.tax_personal_info = request.form['indiv22']
        my_data.specific_info = request.form['indiv23']
        my_data.engage_account = request.form['indiv24']
        my_data.engage_leading = request.form['indiv25']
        my_data.note = request.form['indiv26']
        my_data.timemark = datetime.utcnow()
        my_data.phone1digit = (request.form['indiv7']).replace('-','')
        my_data.phone2digit = (request.form['indiv8']).replace('-','')

        name = []
        for x in range(19):
            name.append(request.form['indiv' + str(x+27)])
        contact_corp = utility.get_id_from_name(name, 0, 3)
        director_corp = utility.get_id_from_name(name, 3, 3)
        sharehold_corp = utility.get_id_from_name(name, 6, 3)
        spouse = utility.get_id_from_name(name, 9, 2)
        parent = utility.get_id_from_name(name, 11, 4)
        child = utility.get_id_from_name(name, 15, 4)

        if contact_corp == []:
            my_data.contact_corp = ""
        else:
            utility.indiv_to_corp_contact(contact_corp, id, 1, value0_corp[0])
            my_data.contact_corp = ",".join(contact_corp)

        if director_corp == []:
            my_data.director_corp = ""
        else:
            utility.indiv_to_corp_director(director_corp, id, 1, value0_corp[1] )
            my_data.director_corp = ",".join(director_corp)

        if sharehold_corp == []:
            my_data.sharehold_corp = ""
        else:
            utility.indiv_to_corp_shareholder(sharehold_corp, id, 1, value0_corp[2])
            my_data.sharehold_corp = ",".join(sharehold_corp)

        if spouse == []:
            my_data.spouse = ""
        else:
            utility.indiv_to_spouse(spouse, id, 1, value0_indiv[0])
            my_data.spouse = ",".join(spouse)

        if parent == []:
            my_data.parent = ""
        else:
            utility.parent_to_child(parent, id, 1, value0_indiv[1])
            my_data.parent = ",".join(parent)

        if child == []:
            my_data.child = ""
        else:
            utility.child_to_parent(child, id, 1, value0_indiv[2])
            my_data.child = ",".join(child)

        db.session.commit()
        flash("Individual Updated Successfully")
        return redirect(url_for('individual'))

    return render_template(
        'individual_edit.html',
        title='Edit_Individual',
        indiv_data = my_data,
        corp_dropdown = corp_dropdown,
        indiv_dropdown = indiv_dropdown,
        corp_list = corp_list,
        indiv_relation_list = indiv_relation_list
    )

@app.route('/individual_del', methods=['GET', 'POST'])
@app.route('/individual_del/<int:id>', methods=['GET', 'POST'])
def individual_del(id):
    my_data = Individual.query.get(id)
    if request.method == 'POST':

        if len(my_data.contact_corp) > 0:
            utility.indiv_to_corp_contact('', id, 2, my_data.contact_corp)

        if len(my_data.director_corp) > 0:
            utility.indiv_to_corp_director('', id, 2, my_data.director_corp)

        if len(my_data.sharehold_corp) > 0:
            utility.indiv_to_corp_shareholder('', id, 2, my_data.sharehold_corp)

        if len(my_data.spouse) > 0:
            utility.indiv_to_spouse('', id, 2, my_data.spouse)
 
        if len(my_data.parent) > 0:
            utility.parent_to_child('', id, 2, my_data.parent)
  
        if len(my_data.child) > 0:
            utility.child_to_parent('', id, 2, my_data.child)

        db.session.delete(my_data)
        db.session.commit()
        flash("Individual Deleted Successfully")
        return redirect(url_for('individual'))

    return render_template(
        'individual_edit.html',
        indiv_data = my_data,
        title='Edit_Individual'
    )

@app.route('/task', methods=['GET', 'POST'])
@login_required
def task():
    ''' task/job information'''
    tasks = Task.query.order_by(Task.periodend.asc()).all()
    return render_template(
        'task.html',
        tasks = tasks,
        title='Task'
    )

@app.route('/task_add', methods=['GET', 'POST'])
@login_required
def task_add():
    corp_dropdown = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp1, Corporation.corp2)
    indiv_dropdown = Individual.query.with_entities(Individual.indiv_id, Individual.prefix, Individual.last_name, Individual.first_name, Individual.sin)
    jobtype_dropdown = Job_type.query.with_entities(Job_type.job_id, Job_type.short_code, Job_type.name)
    if request.method == 'POST':
        tmp = request.form['taskedit1']
        arr = utility.fix_data_missing(tmp, 3)
        client_corp_id = utility.convert_to_int(arr[0])
        client_corp_name = arr[2]
        client_corp_bussi_no = arr[1]
        tmp = request.form['taskedit2']
        arr = utility.fix_data_missing(tmp, 3)
        client_indiv_id = utility.convert_to_int(arr[0])
        client_indiv_name = arr[1]
        client_indiv_sin = arr[2]
        tmp = request.form['taskedit6']
        arr = utility.fix_data_missing(tmp, 3)
        jobtype_id = utility.convert_to_int(arr[0])
        jobtype_code = arr[1]
        periodend = request.form['taskedit3']
        responsible = request.form['taskedit7']
        startdate = request.form['taskedit4']
        enddate = request.form['taskedit5']
        status = request.form['taskedit9']
        details = request.form['taskedit8']
        recurrence = request.form['taskedit11']
        priority = request.form['taskedit10']
        worktime = round(float(request.form['taskedit12']), 2)
        renewperiod = ""
        renewstartdate = ""
        renewenddate = ""
        # fmt = "%Y-%m-%d %H:%M:%S %Z%z"
        fmt = "%Y-%m-%d"
        now_time = datetime.now(timezone('America/Toronto'))
        createdate = now_time.strftime(fmt)
        serialno = random()

        if recurrence == 'Annually':
            num_mon = 12
        elif recurrence == 'Quarterly':
            num_mon = 3
        elif recurrence == 'Monthly':
            num_mon = 1
        renewperiod = datetime.strptime(request.form['taskedit3'], '%Y-%m-%d') + relativedelta(months=num_mon)
        renewstartdate = datetime.strptime(request.form['taskedit4'], '%Y-%m-%d') + relativedelta(months=num_mon)
        renewenddate = datetime.strptime(request.form['taskedit5'], '%Y-%m-%d') + relativedelta(months=num_mon)
        renewperiod = renewperiod.strftime("%Y-%m-%d")
        renewstartdate = renewstartdate.strftime("%Y-%m-%d")
        renewenddate = renewenddate.strftime("%Y-%m-%d")

        my_data = Task(client_corp_id, client_corp_name, client_corp_bussi_no, client_indiv_id, client_indiv_name, client_indiv_sin, jobtype_id, jobtype_code, periodend, responsible, startdate, enddate, status, details, recurrence, priority, worktime, renewperiod, renewstartdate, renewenddate, createdate, serialno)
        db.session.add(my_data)
        db.session.commit()
        flash("Add task Successfully")
        return redirect(url_for('task'))

    return render_template(
        'task_add.html',
        corp_dropdown = corp_dropdown,
        indiv_dropdown = indiv_dropdown,
        jobtype_dropdown = jobtype_dropdown,
        title = 'Add_new_task'
    )

@app.route('/task_renew', methods=['GET', 'POST'])
@app.route('/task_renew/<int:id>', methods=['GET', 'POST'])
@login_required
def task_renew(id):
    corp_dropdown = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp1, Corporation.corp2)
    indiv_dropdown = Individual.query.with_entities(Individual.indiv_id, Individual.prefix, Individual.last_name, Individual.first_name, Individual.sin)
    jobtype_dropdown = Job_type.query.with_entities(Job_type.job_id, Job_type.short_code, Job_type.name)
    my_data = Task.query.get(id)   
    corp_idx = db.session.query(Corporation).with_entities(func.count(Corporation.corp_id)).filter(Corporation.corp_id <= my_data.client_corp_id).scalar()
    max = db.session.query(Corporation).with_entities(func.max(Corporation.corp_id)).scalar()
    if max < corp_idx:
        corp_idx = 0
    indiv_idx = db.session.query(Individual).with_entities(func.count(Individual.indiv_id)).filter(Individual.indiv_id <= my_data.client_indiv_id).scalar()
    max = db.session.query(Individual).with_entities(func.max(Individual.indiv_id)).scalar()
    if max < indiv_idx:
        indiv_idx = 0
    type_idx = db.session.query(Job_type).with_entities(func.count(Job_type.job_id)).filter(Job_type.job_id <= my_data.jobtype_id).scalar()
    max = db.session.query(Job_type).with_entities(func.max(Job_type.job_id)).scalar()
    if max < type_idx:
        type_idx = 0
    
    if request.method == 'POST':
        tmp = request.form['taskedit1']
        arr = utility.fix_data_missing(tmp, 3)
        client_corp_id = utility.convert_to_int(arr[0])
        client_corp_name = arr[2]
        client_corp_bussi_no = arr[1]
        tmp = request.form['taskedit2']
        arr = utility.fix_data_missing(tmp, 3)
        client_indiv_id = utility.convert_to_int(arr[0])
        client_indiv_name = arr[1]
        client_indiv_sin = arr[2]
        tmp = request.form['taskedit6']
        arr = utility.fix_data_missing(tmp, 3)
        jobtype_id = utility.convert_to_int(arr[0])
        jobtype_code = arr[1]
        periodend = request.form['taskedit3']
        responsible = request.form['taskedit7']
        startdate = request.form['taskedit4']
        enddate = request.form['taskedit5']
        status = request.form['taskedit9']
        details = request.form['taskedit8']
        recurrence = request.form['taskedit11']
        priority = request.form['taskedit10']
        worktime = round(float(request.form['taskedit12']), 2)
        renewperiod = ""
        renewstartdate = ""
        renewenddate = ""
        # fmt = "%Y-%m-%d %H:%M:%S %Z%z"
        fmt = "%Y-%m-%d"
        now_time = datetime.now(timezone('America/Toronto'))
        createdate = now_time.strftime(fmt)
        serialno = random()

        if recurrence == 'Annually':
            num_mon = 12
        elif recurrence == 'Quarterly':
            num_mon = 3
        elif recurrence == 'Monthly':
            num_mon = 1
        renewperiod = datetime.strptime(request.form['taskedit3'], '%Y-%m-%d') + relativedelta(months=num_mon)
        renewstartdate = datetime.strptime(request.form['taskedit4'], '%Y-%m-%d') + relativedelta(months=num_mon)
        renewenddate = datetime.strptime(request.form['taskedit5'], '%Y-%m-%d') + relativedelta(months=num_mon)
        renewperiod = renewperiod.strftime("%Y-%m-%d")
        renewstartdate = renewstartdate.strftime("%Y-%m-%d")
        renewenddate = renewenddate.strftime("%Y-%m-%d")

        my_data = Task(client_corp_id, client_corp_name, client_corp_bussi_no, client_indiv_id, client_indiv_name, client_indiv_sin, jobtype_id,jobtype_code, periodend, responsible, startdate, enddate, status, details, recurrence, priority, worktime, renewperiod, renewstartdate, renewenddate, createdate, serialno)
        db.session.add(my_data)
        db.session.commit()
        flash("Task Renewed Successfully, An New Task Inserted!")
        return redirect(url_for('task'))

    return render_template(
        'task_renew.html',
        corp_dropdown = corp_dropdown,
        indiv_dropdown = indiv_dropdown,
        jobtype_dropdown = jobtype_dropdown,
        task_data = my_data,
        corp_idx = corp_idx,
        indiv_idx = indiv_idx,
        type_idx = type_idx,
        title = 'Renew_task'
    )

@app.route('/task_edit', methods=['GET', 'POST'])
@app.route('/task_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def task_edit(id):
    corp_dropdown = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp1, Corporation.corp2)
    indiv_dropdown = Individual.query.with_entities(Individual.indiv_id, Individual.prefix, Individual.last_name, Individual.first_name, Individual.sin)
    jobtype_dropdown = Job_type.query.with_entities(Job_type.job_id, Job_type.short_code, Job_type.name)
    my_data = Task.query.get(id)
    corp_idx = db.session.query(Corporation).with_entities(func.count(Corporation.corp_id)).filter(Corporation.corp_id <= my_data.client_corp_id).scalar()
    max = db.session.query(Corporation).with_entities(func.max(Corporation.corp_id)).scalar()
    if max < corp_idx:
        corp_idx = 0
    indiv_idx = db.session.query(Individual).with_entities(func.count(Individual.indiv_id)).filter(Individual.indiv_id <= my_data.client_indiv_id).scalar()
    max = db.session.query(Individual).with_entities(func.max(Individual.indiv_id)).scalar()
    if max < indiv_idx:
        indiv_idx = 0
    type_idx = db.session.query(Job_type).with_entities(func.count(Job_type.job_id)).filter(Job_type.job_id <= my_data.jobtype_id).scalar()
    max = db.session.query(Job_type).with_entities(func.max(Job_type.job_id)).scalar()
    if max < type_idx:
        type_idx = 0
    if request.method == 'POST':
        tmp = request.form['taskedit1']
        arr = utility.fix_data_missing(tmp, 3)
        my_data.client_corp_id = utility.convert_to_int(arr[0])
        my_data.client_corp_name = arr[2]
        my_data.client_corp_bussi_no = arr[1]
        tmp = request.form['taskedit2']
        arr = utility.fix_data_missing(tmp, 3)
        my_data.client_indiv_id = utility.convert_to_int(arr[0])
        my_data.client_indiv_name = arr[1]
        my_data.client_indiv_sin = arr[2]
        tmp = request.form['taskedit6']
        arr = utility.fix_data_missing(tmp, 3)
        my_data.jobtype_id = utility.convert_to_int(arr[0])
        my_data.jobtype_code = arr[1]
        my_data.periodend = request.form['taskedit3']
        my_data.responsible = request.form['taskedit7']
        my_data.startdate = request.form['taskedit4']
        my_data.enddate = request.form['taskedit5']
        my_data.status = request.form['taskedit9']
        my_data.details = request.form['taskedit8']
        my_data.recurrence = request.form['taskedit11']
        my_data.priority = request.form['taskedit10']
        my_data.worktime = round(float(request.form['taskedit12']), 2)
        renewperiod = ""
        renewstartdate = ""
        renewenddate = ""
        # fmt = "%Y-%m-%d %H:%M:%S %Z%z"
        fmt = "%Y-%m-%d"
        now_time = datetime.now(timezone('America/Toronto'))
        my_data.createdate = now_time.strftime(fmt)
        my_data.serialno = random()

        if request.form['taskedit11'] == 'Annually':
            num_mon = 12
        elif request.form['taskedit11'] == 'Quarterly':
            num_mon = 3
        elif request.form['taskedit11'] == 'Monthly':
            num_mon = 1
        renewperiod = datetime.strptime(request.form['taskedit3'], '%Y-%m-%d') + relativedelta(months=num_mon)
        renewstartdate = datetime.strptime(request.form['taskedit4'], '%Y-%m-%d') + relativedelta(months=num_mon)
        renewenddate = datetime.strptime(request.form['taskedit5'], '%Y-%m-%d') + relativedelta(months=num_mon)
        my_data.renewperiod = renewperiod.strftime("%Y-%m-%d")
        my_data.renewstartdate = renewstartdate.strftime("%Y-%m-%d")
        my_data.renewenddate = renewenddate.strftime("%Y-%m-%d")
        db.session.commit()
        flash("Task Update Successfully")
        return redirect(url_for('task'))

    return render_template(
        'task_edit.html',
        corp_dropdown = corp_dropdown,
        indiv_dropdown = indiv_dropdown,
        jobtype_dropdown = jobtype_dropdown,
        task_data = my_data,
        corp_idx = corp_idx,
        indiv_idx = indiv_idx,
        type_idx = type_idx,
        title = 'Update_task'
    )

@app.route('/task_del', methods=['GET', 'POST'])
@app.route('/task_del/<int:id>', methods=['GET', 'POST'])
def task_del(id):
    tasks = Task.query.order_by(Task.periodend.asc()).all()
    my_data = Task.query.get(id)
    if request.method == 'POST':
        db.session.delete(my_data)
        db.session.commit()
        flash("Task Deleted Successfully")
        return redirect(url_for('task'))

    return render_template(
        'task.html',
        tasks = tasks,
        title='Task'
        )

@app.route('/dailyentry', methods=['GET', 'POST'])
@login_required
def dailyentry():
    '''display timesheet'''
    list_data = Timesheet.query.all()
    datefilter = db.session.query(Timesheet.startdate).distinct().order_by(Timesheet.startdate.desc()).all()
    userfilter = db.session.query(Timesheet.staff).distinct().order_by(Timesheet.staff.asc()).all()
    if request.method == "POST":
        dateselectfrom = (request.form['dateselectfrom']).replace(' ', '')
        dateselectto = (request.form['dateselectto']).replace(' ', '')
        userselect = (request.form['userselect'])
        attribute = '' if dateselectfrom == '' else 'Timesheet.startdate >= dateselectfrom'
        attribute = attribute if dateselectto == '' else attribute + ', Timesheet.startdate <= dateselectto'
        attribute = attribute if userselect == '' else attribute + ', Timesheet.staff == userselect'
        att = []
        exec('att.append(db.session.query(Timesheet).filter({}).order_by(Timesheet.startdate.desc()).all())'.format(attribute.lstrip(', ')))
        list_data = att[0]
        return render_template(
            'dailyentry.html',
            listdata=list_data,
            datefilter=datefilter,
            userfilter=userfilter,
            dateselectfrom = dateselectfrom,
            dateselectto = dateselectto,
            userselect = userselect,
            title='timesheetlist'
        )
    
    return render_template(
        'dailyentry.html',
        listdata=list_data,
        datefilter=datefilter,
        userfilter=userfilter,
        title='timesheetlist'
    )

@app.route('/dailyentry_add', methods=['GET', 'POST'])
@login_required
def dailyentry_add():
    code_types = activity_code.query.all()
    tasklist = Task.query.all()
    
    # userstr = ['Susan', 'Dannijo', 'Michael', 'Aser', 'Kidden']
    # userstridx = round(random()*4)
    # staff = userstr[userstridx]
    staff = current_user.username
    da = (datetime.now(timezone('America/Toronto'))).strftime("%Y-%m-%d")
    listdata = db.session.query(Timesheet).filter(Timesheet.startdate == da, Timesheet.staff == staff).order_by(Timesheet.timemark.desc()).all()
    rowcount = len(listdata)
    
    if request.method == 'POST':
        data_received = json.loads(request.data)
        formid = data_received['formid']
        if formid == 2:
            # data = request.json
            data = data_received['formdata']
            print("----> " + data[0] + " <---- type(da) is list")
            
            startdate = (data[1])[0:10]
            calhour = data[2]
            adjhour = data[3]
            adjmin = data[4]
            t = (data[5].replace(' ','')).split(':')
            workhour = round((float(t[0]) + float(t[1])/60), 2)
            entryname = data[6]
            entrycontent = data[7]
            activitytype = data[8]
            corp1 = ((data[9].split(" | "))[4]) if (len(data[9].split(" | ")) == 5) else ''
            corp2 = ((data[10].split(" | "))[4]) if (len(data[10].split(" | ")) == 5) else ''
            corp3 = ((data[11].split(" | "))[4]) if (len(data[11].split(" | ")) == 5) else ''
            corp4 = ((data[12].split(" | "))[4]) if (len(data[12].split(" | ")) == 5) else ''
            # userstr = ['Susan', 'Dannijo', 'Michael', 'Aser', 'Kidden']
            # userstridx = round(random()*4)
            # staff = userstr[userstridx]
            # # staff = current_user.username
            timemark = data[13]
            # avgtime = float(data[14])
            jobid = []
            count = 0
            for i in [15, 16, 17, 18]:
                if int(data[i]) in jobid:
                    jobid.append(0)
                else:
                    jobid.append(int(data[i]))

            jobid1 = jobid[0]
            if jobid1 == 0:
                corp1 = ''
            else:
                count += 1
            jobid2 = jobid[1]
            if jobid2 == 0:
                corp2 = ''
            else:
                count += 1
            jobid3 = jobid[2]
            if jobid3 == 0:
                corp3 = ''
            else:
                count += 1
            jobid4 = jobid[3]
            if jobid4 == 0:
                corp4 = ''
            else:
                count += 1 

            avgtime = 0 if count == 0 else round(workhour/count, 2)
            starttime = (data[1])[11:16]
            serialno = random()

            my_data = Timesheet(startdate, calhour, adjhour, adjmin, workhour, entryname, entrycontent, activitytype, corp1, corp2, corp3, corp4, staff, timemark, avgtime, jobid1, jobid2, jobid3, jobid4, starttime, serialno)
            db.session.add(my_data)
            db.session.commit()
            # flash("Dailyentry Inserted Successfully")
            return redirect(url_for('dailyentry'))

    return render_template(
        'dailyentry_add.html',
        code_types = code_types,
        tasklist = tasklist,
        listdata = listdata,
        rowcount = rowcount,
        title = 'Add_new_daily_sheet'
    )

@app.route('/dailyentry_edit', methods=['GET', 'POST'])
@app.route('/dailyentry_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def dailyentry_edit(id):
    ''' update dailyentry information'''
    tasklist = Task.query.with_entities(Task.task_id, Task.periodend, Task.recurrence, Task.jobtype_code, Task.client_corp_name)
    code_types = activity_code.query.all()
    my_data = Timesheet.query.get(id)
    time0 = my_data.workhour
    t = []
    idx = []
    max = db.session.query(Task).with_entities(func.max(Task.task_id)).scalar()
    for i in [1, 2, 3, 4]:
        exec('t.append(my_data.jobid{})'.format(i))
        corp = db.session.query(Task).with_entities(func.count(Task.task_id)).filter(Task.task_id <= t[i-1]).scalar()
        (idx.append(0)) if max < corp else (idx.append(corp))
    if request.method == 'POST':
        my_data.startdate = request.form['timesheetedit1']
        my_data.calhour = request.form['timesheetedit2']
        my_data.adjhour = (request.form['timesheetedit3'].replace(' ','').split(':'))[0]
        my_data.adjmin = (request.form['timesheetedit3'].replace(' ','').split(':'))[1]
        my_data.workhour  = float(request.form['timesheetedit4'])
        my_data.entryname = request.form['timesheetedit5']
        my_data.entrycontent = request.form['timesheetedit6']
        my_data.activitytype = request.form['timesheetedit7']
        my_data.staff = request.form['timesheetedit12']
        my_data.serialno = random()
        t_new = []
        corp = []
        corp_count = 0
        for i in [8,9,10,11]:
            tmp = request.form['timesheetedit' + str(i)].split(' | ')
            if (tmp[0] == '' or (int(tmp[0]) in t_new)):
                t_new.append(0)
                corp.append('')
            else:
                t_new.append(int(tmp[0]))
                corp_count += 1
                corp.append(tmp[4]) if len(tmp)==5 else corp.append('')
        
        my_data.avgtime = round(float(my_data.workhour)/corp_count, 2) if corp_count > 0 else 0
        my_data.jobid1 = t_new[0]
        my_data.jobid2 = t_new[1]
        my_data.jobid3 = t_new[2]
        my_data.jobid4 = t_new[3]
        my_data.corp1 = corp[0]
        my_data.corp2 = corp[1]
        my_data.corp3 = corp[2]
        my_data.corp4 = corp[3]
        for i in t:
            if i not in t_new:
                print('CorporationReport ID: ', i, ' not in new')
                id = db.session.query(CorporationReport).with_entities(CorporationReport.corp_report_id).filter(CorporationReport.jobid == i, CorporationReport.timemark==my_data.timemark).scalar()
                if id is not None and id!=0:
                    report_data = CorporationReport.query.get(id)
                    db.session.delete(report_data)
                    db.session.commit()
                    print('CorporationReport ID: ', i, ' deleted.')
        # update & insert
        for i in range(4):
            if t_new[i] in t and t_new[i]!=0: # update
                id = db.session.query(CorporationReport).with_entities(CorporationReport.corp_report_id).filter(CorporationReport.jobid == t_new[i], CorporationReport.timemark==my_data.timemark).scalar()
                if id is not None and id!=0:
                    report_data = CorporationReport.query.get(id)
                    report_data.corp = corp[i]
                    report_data.startdate = my_data.startdate
                    report_data.entryname = my_data.entryname
                    report_data.activitytype = my_data.activitytype
                    report_data.entrycontent = my_data.entrycontent
                    report_data.workhour = my_data.avgtime
                    report_data.timemark = my_data.timemark
                    report_data.jobid = t_new[i]
                    report_data.serialno = random()
                    db.session.commit()
                    print('update:  ', report_data.corp, report_data.workhour, report_data.jobid )
            elif t_new[i] not in t and t_new[i]!=0: # insert
                if id is not None and id!=0:
                    new_corp = corp[i]
                    new_startdate = my_data.startdate
                    new_entryname = my_data.entryname
                    new_activitytype = my_data.activitytype
                    new_entrycontent = my_data.entrycontent
                    new_workhour = my_data.avgtime
                    new_timemark = my_data.timemark
                    new_jobid = t_new[i]
                    new_serialno = random()
                    new_data = CorporationReport(new_corp, new_startdate, new_entryname, new_activitytype, new_entrycontent, new_workhour, new_timemark, new_jobid, new_serialno)
                    db.session.add(new_data)
                    db.session.commit()
                    print('insert:  ', new_corp, new_workhour, new_jobid )    

        print('new ', t_new, '  old ', t)
        db.session.commit()
        flash("Dailyentry Update Successfully")
        return redirect(url_for('dailyentry'))

    return render_template(
        'dailyentry_edit.html',
        tasklist = tasklist,
        code_types = code_types,
        timesheet = my_data,
        idx = idx,
        title = 'Update_timesheet'
    )

@app.route('/dailyentry_del', methods=['GET', 'POST'])
@app.route('/dailyentry_del/<int:id>', methods=['GET', 'POST'])
def dailyentry_del(id):
    ''' delete dailyentry'''
    list_data = Timesheet.query.all()
    # tasklist = Task.query.all()
    datefilter = db.session.query(Timesheet.startdate).distinct().order_by(Timesheet.startdate.desc()).all()
    userfilter = db.session.query(Timesheet.staff).distinct().order_by(Timesheet.staff.asc()).all()
    my_data = Timesheet.query.get(id)
    if request.method == 'POST':
        db.session.delete(my_data)
        db.session.commit()
        flash("Dailyentry Deleted Successfully")
        return redirect(url_for('dailyentry'))

    return render_template(
        'dailyentry.html',
        listdata=list_data,
        datefilter=datefilter,
        userfilter=userfilter,
        title='timesheetlist'
    )

@app.route('/staff', methods=['GET', 'POST'])
@login_required
def staff():
    '''display staff'''
    list_data = Staff.query.all()
    datefilter = db.session.query(Staff.startdate).distinct().order_by(Staff.startdate.desc()).all()
    userfilter = db.session.query(Staff.name).distinct().order_by(Staff.name.asc()).all()
    if request.method == "POST":
        dateselectfrom = (request.form['dateselectfrom']).replace(' ', '')
        dateselectto = (request.form['dateselectto']).replace(' ', '')
        userselect = (request.form['userselect'])
        attribute = '' if dateselectfrom == '' else 'Staff.startdate >= dateselectfrom'
        attribute = attribute if dateselectto == '' else attribute + ', Staff.startdate <= dateselectto'
        attribute = attribute if userselect == '' else attribute + ', Staff.name == userselect'
        att = []
        exec('att.append(db.session.query(Staff).filter({}).order_by(Staff.startdate.desc()).all())'.format(attribute.lstrip(', ')))
        list_data = att[0]
        return render_template(
            'staff.html',
            listdata=list_data,
            datefilter=datefilter,
            userfilter=userfilter,
            dateselectfrom = dateselectfrom,
            dateselectto = dateselectto,
            userselect = userselect,
            title='Staff'
        )
    return render_template(
        'staff.html',
        listdata=list_data,
        datefilter=datefilter,
        userfilter=userfilter,
        title='Staff'
    )

@app.route('/corporation_report', methods=['GET', 'POST'])
@login_required
def corporation_report():
    '''display corporation_report'''
    list_data = CorporationReport.query.all()
    datefilter = db.session.query(CorporationReport.startdate).distinct().order_by(CorporationReport.startdate.desc()).all()
    userfilter = db.session.query(CorporationReport.corp).distinct().order_by(CorporationReport.corp.asc()).all()
    if request.method == "POST":
        dateselectfrom = (request.form['dateselectfrom']).replace(' ', '')
        dateselectto = (request.form['dateselectto']).replace(' ', '')
        userselect = (request.form['userselect'])
        attribute = '' if dateselectfrom == '' else 'CorporationReport.startdate >= dateselectfrom'
        attribute = attribute if dateselectto == '' else attribute + ', CorporationReport.startdate <= dateselectto'
        attribute = attribute if userselect == '' else attribute + ', CorporationReport.corp == userselect'
        att = []
        exec('att.append(db.session.query(CorporationReport).filter({}).order_by(CorporationReport.startdate.desc()).all())'.format(attribute.lstrip(', ')))
        list_data = att[0]
        return render_template(
            'corporation_report.html',
            listdata=list_data,
            datefilter=datefilter,
            userfilter=userfilter,
            dateselectfrom = dateselectfrom,
            dateselectto = dateselectto,
            userselect = userselect,
            title='CorporationReport'
        )
    return render_template(
        'corporation_report.html',
        listdata=list_data,
        datefilter=datefilter,
        userfilter=userfilter,
        title='CorporationReport'
    )

@app.route('/search', methods=['GET', 'POST'])
def search(): # sample 1181,8805,318805
    if request.method == 'POST':
        tag = (request.form['searchnumber']).replace(' ', '').replace('-', '')
        search = "%{}%".format(tag)
        list_indiv = db.session.query(Individual).with_entities(Individual.prefix, Individual.last_name, Individual.first_name, Individual.phone1, Individual.phone2).filter(or_(Individual.phone1digit.like(search), Individual.phone2digit.like(search)))
        list_corp = Corporation.query.with_entities(Corporation.corp1, Corporation.corp2, Corporation.corp20, Corporation.corp21).filter(or_(Corporation.corp201.like(search), Corporation.corp211.like(search)))
        return render_template(
            'search.html',
            list_indiv = list_indiv,
            list_corp = list_corp,
            title = 'Search'
        )
    return render_template(
        'search.html',
        title = 'Search'
    )

@app.route('/download', methods=['GET', 'POST'])
@login_required
def download(): 
    
    formid = request.args.get('formid', 1, type=int)
    if request.method == 'POST' and formid == 1:
        category = request.form['category']
        category = 'Corporation' if category == '' else category
        data = utility.download_munu(category)
        filtertxt = data[0]
        filterdata = data[1]
        filterselect = ['','','']
        return render_template(
            'download.html',
            category = category,
            filtertxt = filtertxt,
            filterdata = filterdata,
            filterselect = filterselect,
            message = '',
            title = 'Download'
        )

    elif request.method == 'POST' and formid == 2:
        print('---- formid = 2 -----')
        filterselect = ['','','']
        category = request.form['filter0']
        data = utility.download_munu(category)
        filtertxt = data[0]
        filterdata = data[1]
        filterselect[0] = request.form['filter1']
        filterselect[1] = request.form['filter2']
        filterselect[2] = request.form['filter3']
        da = (datetime.now(timezone('America/Toronto'))).strftime("%Y-%m-%d")
        filename = category + '-' + da + '.xlsx'
        message = ''
        if category != '':
            utility.excel_export(category, filterselect, filename)
            message = 'Download "' + filename + '" successfully.' 
            path = "/var/www/html/app/static/download/"
            list = os.listdir(path)
            for f in list:
                if (not f == filename):
                    os.remove(path + f)
            try:
                return send_from_directory(path, filename=filename, as_attachment=True)
            except FileNotFoundError:
                abort(404)
                
        # return render_template(
        #     'download.html',
        #     category = category,
        #     filtertxt = filtertxt,
        #     filterdata = filterdata,
        #     filterselect = filterselect,
        #     message = message,
        #     title = 'Download'
        # )
    else:
        filtertxt = ['','','']
        filterdata = ['','','']
        filterselect = ['','','']
        return render_template(
            'download.html',
            category = '',
            filtertxt = filtertxt,
            filterdata = filterdata,
            filterselect = filterselect,
            message = '',
            title = 'Download'
        )

@app.route('/importdata', methods=['GET', 'POST'])
@login_required
def importdata():
    utility.fix_address()
    # utility.import_excel_indiv()
    return render_template(
        'index.html',
        title='Home'
    )

@app.route('/indiv_chart', methods=['GET', 'POST'])
@login_required
def indiv_chart():
    my_idx = 0
    per_list = [0,0,0,0]
    # corp = Corporation.query.with_entities(Corporation.corp_id, Corporation.corp1, Corporation.corp2)
    indiv = Individual.query.with_entities(Individual.indiv_id, Individual.sin, Individual.last_name, Individual.first_name)
    if request.method == 'POST':
        my_idx = 0
        my_indiv = request.form['chart1']
        if my_indiv == '':
            my_idx = 0
            per_list = [0,0,0,0]
            indiv_list = []
            corp_list = []
        else:
            my_id = int(my_indiv.split('(ID=')[1].strip(') '))
            my_idx = db.session.query(Individual).with_entities(func.count(Individual.indiv_id)).filter(Individual.indiv_id <= my_id).scalar()
            max = db.session.query(Individual).with_entities(func.max(Individual.indiv_id)).scalar()
            if max < my_idx:
                my_idx = 0
            my_data = db.session.query(Individual).with_entities(Individual.indiv_id, Individual.last_name, Individual.first_name, Individual.contact_corp, Individual.director_corp, Individual.sharehold_corp, Individual.spouse, Individual.parent, Individual.child).filter(Individual.indiv_id==my_id)
            indiv_list = [] # indiv_list[第几组][第几人信息]：
            corp_list = [] # corp_list[第几组][第几人][类型][公司信息]：组(如parents, child)人(parent有2人)类型(contact, director等)
            indiv_list.append([[int(my_data[0].indiv_id), (my_data[0].last_name + ', ' + my_data[0].first_name)]])
            tmp = ([my_data[0].contact_corp, my_data[0].director_corp, my_data[0].sharehold_corp])
            corp_list.append([get_corp_name(tmp)])
            for person in (my_data[0].spouse, my_data[0].parent, my_data[0].child): # 获取parents(4,8)一个组人的id
                # example: my_data[0].spouse == '5,6', my_data[0].parent='7,8', my_data[0].child='9,10,11'
                if person:
                    if len(person)>0 and person != ',':
                        arr = person.split(',') # >>> ['5', '6']
                        arr1 = []
                        arr2 = []
                        for iperson in arr: # >>> ['5']
                            iperson = iperson.replace(' ','')
                            if len(iperson)>0:
                                iperson = int(iperson)
                                per_data = Individual.query.get(iperson)
                                arr1.append([int(per_data.indiv_id), (per_data.last_name + ', ' + per_data.first_name)])
                    # per_data = db.session.query(Individual).with_entities(Individual.indiv_id, Individual.last_name, Individual.first_name, Individual.contact_corp, Individual.director_corp, Individual.sharehold_corp).filter(Individual.indiv_id.in_((arr0))).all() 
                    # 获取parents(4,8)一个组人对应的人名，和公司(contact, director, shareholder)
                    # 格式是[(第1人ID，名字，contact(' '), direct(' '), shareholder(' ')), (第2人ID，....),  (第3人ID，....) ]
                    # >>> per_data = [(5, 'CAI', 'Zhiyuan', '12,6', '13,7', '14'), (6, 'CHAOLEI', 'YI', '314,6', '13,7', '14')]
                    # 注意：(1) filter(Individual.indiv_id.in_((12，6)))，in_后面是2个括号((
                    # 注意：(2) in_((是数组数字))，如果是字串，比如'12, 6'，那么得出结果是in(1,2,6)
                    # 注意：(3) 返回的顺序是由小到大自动排列，相当于in(6, 12) 
                                # 人名和ID存入arr1 >>> [[5, 'CAI, Zhiyuan']]
                                tmp = ([per_data.contact_corp, per_data.director_corp, per_data.sharehold_corp])
                                # 公司的ID存入了arr2，下面要把ID换成公司的ID和名字 >>> tmp = ['12,6', '13,7', '14']
                                arr2.append(get_corp_name(tmp))
                    indiv_list.append(arr1)
                    corp_list.append(arr2)
                else:
                    indiv_list.append('')
                    corp_list.append('')
        
        for i in range(len(indiv_list)):
            per_list[i] = len(indiv_list[i])
        print(f"per_list = {per_list}")
        return render_template(
            'indiv_chart.html',
            indiv_data = indiv,
            per_list = per_list,
            indiv_list = indiv_list,
            corp_list = corp_list,
            my_idx = my_idx
        )
    else:
        return render_template(
            'indiv_chart.html',
            indiv_data = indiv,
            per_list = per_list,
            indiv_list = [],
            corp_list = [],
            my_idx = my_idx
        )

@app.route('/corp_chart', methods=['GET', 'POST'])
@login_required
def corp_chart():
    return render_template(
        'corp_chart.html'
    )

@app.route("/get_report")
@app.route("/get_report/<path:path>")
def get_report(path):
    try:
        return send_from_directory(app.config["CLIENT_REPORTS"], filename=path, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get_image")
@app.route("/get_image/<image_name>")
def get_image(image_name):

    # path = app.config["CLIENT_IMAGES"]
    # list = os.listdir(path)
    # print(type(list), list)
    # print('image_name', image_name)
    # for f in list:
    #     if (not f == image_name):
    #         os.remove(path +'/' + f)
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get_csv")
@app.route("/get_csv/<csv_id>")
def get_csv(csv_id):
    filename = f"{csv_id}.csv"
    try:
        return send_from_directory(app.config["CLIENT_CSV"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/timesheet')
@login_required
def timesheet():
    all_data = activity_code.query.all()
    # list_data = Timesheet.query.join(Task, Timesheet.id == Task.id).add_columns(Timesheet.id, Timesheet.entryname, Timesheet.corp1, Task.id, Task.client)
    # list_data = Timesheet.query.join(Task, Timesheet.id == Task.id).all()
    # list_data = db.session.query(Timesheet.id, Timesheet.entryname, Timesheet.corp1, Task.id, Task.client).filter(Timesheet.id == Task.id).all()
    # print(list_data[0])
    # print(list_data[1])
    list_data = Timesheet.query.all()
    tasklist = Task.query.all()
    return render_template(
        'timesheet.html',
        code_types=all_data,
        list=list_data,
        tasklist = tasklist,
        title='timesheet'
    )

@app.route('/timesheetInsertion', methods=['POST'])
@login_required
def timesheetInsertion():
    if request.method == 'POST':
        data = request.json
        print("----> " + data[0] + " <---- type(da) is list")
        startdate = (data[1])[0:10] # 注意 string[start: end: step] 中end是那位是不包含的，所以('0123')[0:2] ==> '01'
        calhour = data[2]
        adjhour = data[3]
        adjmin = data[4]
        workhour = data[5]
        entryname = data[6]
        entrycontent = data[7]
        activitytype = data[8]
        corp1 = (data[9].split(" | "))[3]
        corp2 = (data[10].split(" | "))[3]
        corp3 = (data[11].split(" | "))[3]
        corp4 = (data[12].split(" | "))[3]
        userstr = ['Susan', 'Dannijo', 'Michael', 'Aser', 'Kidden']
        userstridx = round(random()*4)
        staff = userstr[userstridx]
        # staff = "Susan" #current_user.username
        timemark = data[13]
        avgtime = float(data[14])
        jobid1 = int(data[15])
        jobid2 = int(data[16])
        jobid3 = int(data[17])
        jobid4 = int(data[18])
        starttime = (data[1])[11:16]
        serialno = random()

        my_data = Timesheet(
            startdate,
            calhour,
            adjhour,
            adjmin,
            workhour,
            entryname,
            entrycontent,
            activitytype,
            corp1,
            corp2,
            corp3,
            corp4,
            staff,
            timemark,
            avgtime,
            jobid1,
            jobid2,
            jobid3,
            jobid4,
            starttime,
            serialno
        )
        db.session.add(my_data)
        db.session.commit()
        # flash("Dailyentry Inserted Successfully")
    return redirect(url_for("timesheet"))

@app.route('/timesheetlist', methods=['GET','POST'], defaults={"page":1})
@app.route('/timesheetlist/<int:page>', methods=['GET','POST'])
@login_required
def timesheetlist(page):
    '''display timesheet'''
    page = page
    pages = 10
    c = session.get("cc")

    print(c)
    if (session.get("filterstatus") is None):
        print("check session")
    print(session.get("filterstatus"))
    # status = session.get("filterstatus")
    # if ( status is None):
    #     print("enter into session...")
    #     list_data = Timesheet.query.paginate(page, per_page=pages, error_out=True)
    # else:
    #     list_data = Timesheet.query.filter(Timesheet.staff == "Susan").paginate(per_page=pages, error_out=True)
    
    list_data = Timesheet.query.paginate(page, per_page=pages, error_out=True)
    tasklist = Task.query.all()
    datefilter = db.session.query(Timesheet.startdate).distinct().order_by(Timesheet.startdate.desc()).all()
    userfilter = db.session.query(Timesheet.staff).distinct().order_by(Timesheet.staff.asc()).all()

    if request.method == "POST":
        status = 1
        dateselect = (request.form['dateselect']).replace(" ","")
        userselect = (request.form['userselect']).replace(" ","")
        if dateselect != "" and userselect != "":
            list_data = Timesheet.query.filter(Timesheet.startdate == dateselect, Timesheet.staff == userselect).paginate(per_page=pages, error_out=True)
        elif dateselect != "" and userselect == "":
            list_data = Timesheet.query.filter(Timesheet.startdate == dateselect).paginate(per_page=pages, error_out=True)
        elif dateselect == "" and userselect != "":
            list_data = Timesheet.query.filter(Timesheet.staff == userselect).paginate(per_page=pages, error_out=True)
        
        # session['filterstatus'] = 'usingfilter'

    return render_template(
        'timesheetlist.html',
        listdata=list_data,
        tasklist=tasklist,
        datefilter=datefilter,
        userfilter=userfilter,
        title='timesheetlist'
    )

@app.route('/Corp_report_old', methods=['GET','POST'], defaults={"page":1})
@app.route('/Corp_report_old/<int:page>', methods=['GET','POST'])
def Corp_report_old(page):
    page = page
    pages = 10
    list_data = CorporationReport.query.paginate(page, per_page=pages, error_out=True)
    tasklist = Task.query.all()
    datefilter = db.session.query(CorporationReport.date).distinct().order_by(CorporationReport.date.desc()).all()
    corpfilter = db.session.query(CorporationReport.corp).distinct().order_by(CorporationReport.corp.asc()).all()
    return render_template(
        'Corp_report.html',
        listdata=list_data,
        tasklist=tasklist,
        datefilter=datefilter,
        corpfilter=corpfilter,
        title='CorporationReport'
    )

@app.route('/staff_old', methods=['GET','POST'], defaults={"page":1})
@app.route('/staff_old/<int:page>', methods=['GET','POST'])
def staff_old(page):
    page = page
    pages = 10
    # list_data = Staff.query.paginate(page, per_page=pages, error_out=True)
    list_data = db.session.query(Staff.name, Staff.date, Staff.workhour).distinct(Staff.name, Staff.date).order_by(Staff.name.asc(), Staff.date.desc()).all()
    print(list_data)
    tasklist = Task.query.all()
    datefilter = db.session.query(Staff.date).distinct().order_by(Staff.date.desc()).all()
    stafffilter = db.session.query(Staff.name).distinct().order_by(Staff.name.asc()).all()
    return render_template(
        'staff.html',
        listdata=list_data,
        tasklist=tasklist,
        datefilter=datefilter,
        stafffilter=stafffilter,
        title='staff'
    )

# @app.route('/timesheet_tempdata', methods=['GET', 'POST'])
# def timesheet_tempdata():
    # if request.method == 'POST':
    #     rsl = request.json # rsl is list type, very similar to array
    #     # read data from db
    #     da = TimesheetTempData.query.filter_by(t0 = rsl[0]).first()
    #     if (type(da) == type(None)) :
    #         my_data = TimesheetTempData(t0 = rsl[0],
    #         t1 = rsl[1],
    #         t2 = rsl[2],
    #         t3 = rsl[3],
    #         t4 = rsl[4],
    #         t5 = rsl[5],
    #         t6 = rsl[6],
    #         t7 = rsl[7],
    #         t8 = rsl[8],
    #         t9 = rsl[9],
    #         t10 = rsl[10],
    #         t11 = rsl[11],
    #         t12 = rsl[12],
    #         t13 = 1)
    #         db.session.add(my_data)
    #         db.session.commit()
    #         #flash("Task Renew Successfully")
    #     if (da.t0 == rsl[0]) :
    #         my_data = TimesheetTempData.query.get(rsl[0])
    #         my_data.t1 = rsl[1]
    #         my_data.t2 = rsl[2]
    #         my_data.t3 = rsl[3]
    #         my_data.t4 = rsl[4]
    #         my_data.t5 = rsl[5]
    #         my_data.t6 = rsl[6]
    #         my_data.t7 = rsl[7]
    #         my_data.t8 = rsl[8]
    #         my_data.t9 = rsl[9]
    #         my_data.t10 = rsl[10]
    #         my_data.t11 = rsl[11]
    #         my_data.t12 = rsl[12]
    #         my_data.t13 = 1
    #         db.session.commit()
    #         #flash("Task Renew Successfully")
    #     return "data is saved."

@app.route('/timesheetupdate', methods=['GET', 'POST'])
def timesheetupdate():
    ''' update timesheet daily entry '''
    if request.method == 'POST':
        updatedata = Timesheet.query.get(request.form.get('id'))
        updatedata.date = request.form['timesheet1-1']
        updatedata.staff = request.form['timesheet1-2']
        updatedata.starttime = request.form['timesheet1-3']
        updatedata.calhr = request.form['timesheet1-4']
        updatedata.workhr = request.form['timesheet1-6']
        updatedata.comment = request.form['timesheet1-15']
        updatedata.entryname = request.form['timesheet1-7']
        updatedata.activitytype = request.form['timesheet1-8']
        updatedata.taskcode = request.form['timesheet1-9']
        updatedata.corp1 = request.form['timesheet1-10']
        updatedata.corp2 = request.form['timesheet1-12']
        updatedata.corp3 = request.form['timesheet1-13']
        updatedata.corp4 = request.form['timesheet1-14']
        updatedata.entrycontent = request.form['timesheet1-11']
        db.session.commit()
        flash("Employee Updated Successfully")
    return redirect(url_for('timesheet'))

@app.route('/postmethod01', methods=['POST']) 
def get_post01():
    
    jsdata = request.form['js_data']
    # json.loads(jsdata)[0]
    print("*****route*******" + jsdata)
    return jsdata

@app.route('/postmethod02', methods=['POST']) 
def get_post02():
    
    if request.method == 'POST':
        asd = request.json
        print(asd)
        if 'key1' in asd:
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return render_template("createform.html")
    # r

@app.route('/temp')
def temp():
    return render_template(
        'temp.html',
        title='temp'
    )

@app.route('/learning_js_pass_data')
def js_pass_data():
    return render_template(
        'learning_js_pass_data.html',
        title='temp'
    )

@app.route('/multipleForms', methods=['GET','POST'])
def multipleForms():
    
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'add-1':
            name = request.form['box1']
        elif request.form['btn_identifier'] == 'add-2':
            name = request.form['box2']

        my_data = Mulform(name)
        db.session.add(my_data)
        db.session.commit()
        flash("Dailyentry Inserted Successfully")

    return render_template(
        'multipleForms.html',
        title='multipleForms'
    )

@app.route('/input_validation')
def input_validation():
    return render_template(
        'learning_input_validation.html'
    )
# **** following is to try Data table CRUD functions ******
# T
@app.route('/data_crud')
def data_crud():
    all_data = Data_table.query.all() # Data_table is defined in models.py
    return render_template(
        'data_crud.html',
        employees=all_data,
        title='data_crud'
    )
#this rms
@app.route('/insertion', methods=['POST'])
def insertion():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
 
        my_data = Data_table(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        flash("Employee Inserted Successfully")
        return redirect(url_for('data_crud'))
#this is our uloyee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data_table.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('data_crud'))
#This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete():
    my_data = Data_table.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('data_crud'))
