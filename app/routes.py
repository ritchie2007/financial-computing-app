from datetime import datetime
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import desc # for table.order_by(Task.enddate).all()
from sqlalchemy import asc
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, WebNavForm
from app.models import User, Data_table, activity_code, Task, Timesheet, Mulform
from random import random
#from app import dateCalculate
from time import strftime, strptime, localtime
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from flask import make_response
import json

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    else:
        pass

@app.route('/')
@app.route(
    '/index',
    methods=['GET', 'POST']
)
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
@app.route(
    '/login',
    methods=['GET', 'POST']
)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user is None:
                flash('Username does not exist')
                return redirect(url_for('login'))
            elif user.check_password(form.password.data) is False:
                flash('Invalid password')
                return redirect(url_for('login'))
            else:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')

                if not next_page or url_parse(next_page).netloc != '':
                    return redirect(url_for('index'))
                else:
                    return redirect(next_page)
        else:
            return render_template(
                'login.html',
                title='Login',
                form=form
            )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route(
    '/register',
    methods=['GET', 'POST']
)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    else:
        form = RegistrationForm()

        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
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

@app.route(
    '/edit_profile',
    methods=['GET', 'POST']
)
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

@app.route(
    '/corporate'
)
def corporate():
    return render_template(
        'corporate.html',
        title='Corporate'
    )

@app.route(
    '/Corp_Spec'
)
def corp_spec():
    return render_template(
        'corp_spec.html',
        title='Corp_Spec'
    )

@app.route('/task')
def task():
    all_data = Task.query.order_by(Task.periodend.asc()).all()
    return render_template(
        'task.html',
        tasks=all_data,
        title='Task'
        )

@app.route('/taskinsertion', methods=['GET','POST'])
def taskinsertion():
    if request.method == 'POST':
        client = request.form['taskedit-1']
        jobtype = request.form['taskedit-2']
        details = request.form['taskedit-4']
        status = request.form['taskedit-7']
        priority = request.form['taskedit-8']
        recurrence = request.form['taskedit-9']
        jobowner = request.form['taskedit-10']
        validation = random()
        worktime = request.form['taskedit-11']
        periodend = request.form['taskedit-31']
        nextstartdate = request.form['taskedit-51']
        nextenddate = request.form['taskedit-61']

        if periodend == '':
            n = 0
            if recurrence == 'y' or recurrence == 'Y':
                n = 12
            elif recurrence == 'q' or recurrence == 'Q':
                n = 3
            elif recurrence == 'm' or recurrence == 'M':
                n = 1
            periodend = datetime.strptime(request.form['taskedit-3'], '%Y-%m-%d') + relativedelta(months=n)
            nextstartdate = datetime.strptime(request.form['taskedit-5'], '%Y-%m-%d') + relativedelta(months=n)
            nextenddate = datetime.strptime(request.form['taskedit-6'], '%Y-%m-%d') + relativedelta(months=n)
            renewperiod = (periodend + relativedelta(months=n)).strftime("%Y-%m-%d")
            renewstartdate = (nextstartdate + relativedelta(months=n)).strftime("%Y-%m-%d")
            renewenddate = (nextenddate + relativedelta(months=n)).strftime("%Y-%m-%d")
            periodend = periodend.strftime("%Y-%m-%d")
            nextstartdate = nextstartdate.strftime("%Y-%m-%d")
            nextenddate = nextenddate.strftime("%Y-%m-%d")

        my_data = Task(
            client,
            jobtype,
            periodend,
            details,
            nextstartdate,
            nextenddate,
            status,
            priority,
            recurrence,
            jobowner,
            validation,
            worktime,
            renewperiod,
            renewstartdate,
            renewenddate
        )
        db.session.add(my_data)
        db.session.commit()
        flash("Task Renew Successfully")
    return redirect(url_for('task'))

@app.route('/taskupdate', methods=['POST'])
def taskupdate():
    if request.method == 'POST':
        my_data = Task.query.get(request.form.get('id'))
        my_data.client = request.form['taskedit-1']
        my_data.jobtype = request.form['taskedit-2']
        my_data.periodend = request.form['taskedit-3']
        my_data.details = request.form['taskedit-4']
        my_data.nextstartdate = request.form['taskedit-5']
        my_data.nextenddate = request.form['taskedit-6']
        my_data.status = request.form['taskedit-7']
        my_data.priority = request.form['taskedit-8']
        my_data.recurrence = request.form['taskedit-9']
        my_data.jobowner = request.form['taskedit-10']
        my_data.validation = random()
        my_data.worktime = request.form['taskedit-11']
        
        db.session.commit()
        flash("Task Updated Successfully")
        return redirect(url_for('task'))

@app.route('/timesheet', methods=['GET','POST'])
def timesheet():
    all_data = activity_code.query.all()
    list_data = Timesheet.query.all()
    tasklist = Task.query.all()
    if request.method == 'POST':
        #print('\n\nForm data\n{}\n\n'.format(request.form))
        date = request.form['timesheet1-1']
        calhour = request.form['timesheet1-3']
        adjhour = (request.form['timesheet1-41'] + request.form['timesheet1-42'])
        workhour = request.form['timesheet1-5']
        taskname = request.form['timesheet1-6']
        taskcontent = request.form['timesheet1-7']
        tasktype = request.form['timesheet1-8']
        corp1 = request.form['timesheet1-9']
        corp2 = request.form['timesheet1-10']
        corp3 = request.form['timesheet1-11']
        corp4 = request.form['timesheet1-12']
        staff = 'susan'
        validation = random()

        my_data = Timesheet(
            date,
            calhour,
            adjhour,
            workhour,
            taskname,
            taskcontent,
            tasktype,
            corp1,
            corp2,
            corp3,
            corp4,
            staff,
            validation
        )
        db.session.add(my_data)
        db.session.commit()
        flash("Dailyentry Inserted Successfully")
    num = [['tom1','tom2','tom3','tom4'], ['mike1','mike2','mike3'], 'amuxia', 'zhao', 'lisi']
    #num = ['tom1','mike1','mike2','mike3','amuxia', 'zhao', 'lisi']
    return render_template(
        'timesheet.html',
        code_types=all_data,
        list=list_data,
        tasklist = tasklist,
        title='timesheet',
        num = num
    )

@app.route('/timesheetupdate', methods=['GET', 'POST'])
def timesheetupdate():
    if request.method == 'POST':
        da = Timesheet.query.get(request.form.get('id'))
        da.date =request.form['timesheet1-1']
        da.staff =request.form['timesheet1-2']
        da.starttime =request.form['timesheet1-3']
        da.calhr =request.form['timesheet1-4']
        da.workhr =request.form['timesheet1-6']
        da.comment =request.form['timesheet1-15']
        da.taskname =request.form['timesheet1-7']
        da.tasktype =request.form['timesheet1-8']
        da.taskcode =request.form['timesheet1-9']
        da.corp1 =request.form['timesheet1-10']
        da.corp2 =request.form['timesheet1-12']
        da.corp3 =request.form['timesheet1-13']
        da.corp4 =request.form['timesheet1-14']
        da.taskcontent =request.form['timesheet1-11']
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('timesheet'))

@app.route('/postmethod01', methods=['POST']) #接收前台数据 #发送数据到前台
def get_post01():
    # receive a single string from javascript post
    jsdata = request.form['js_data']
    # json.loads(jsdata)[0]
    print ("*****route*******" + jsdata)
    return jsdata

@app.route('/postmethod02', methods=['POST']) #接收前台数据 #发送数据到前台
def get_post02():
    # receive a array from javascript post
    if request.method == 'POST':
        asd = request.json
        print(asd)
        if 'key1' in asd:
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return render_template("createform.html")
    # request.get_data(as_text=True)：获取前端POST请求传过来的 json 数据

@app.route(
    '/temp'
)
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

# **** following is to try Data table CRUD functions ******
# This is the data_table root on all our employee data
@app.route(
    '/data_crud'
)
def data_crud():
    all_data = Data_table.query.all() # Data_table is defined in models.py
    return render_template(
        'data_crud.html',
        employees=all_data,
        title='data_crud'
    )
#this route is for inserting data to mysql database via html forms
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
#this is our update route where we are going to update our employee
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
 