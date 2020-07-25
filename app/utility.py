from random import random
from time import strftime, localtime
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, request, url_for, session, make_response, json
from sqlalchemy import desc, asc # for table.order_by(Task.enddate).all()
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, WebNavForm
from app.models import User, Data_table, activity_code, CorprationReport, Staff, Task, \
    Timesheet, Corporation, Individual, Mulform, TimesheetTempData

def month_offset(start_date, number_of_month):
    return datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(months=number_of_month)
# print(get_today_month(-3))
print(month_offset('2019-01-31', 1))

def get_id_from_name(name, start, count):
    id_list = []
    for i in range(count):
        item = ((name[i+start].split(" | "))[0].lstrip(' ').lstrip('0'))
        if item not in id_list and item != "" :
            id_list.append(item)
    # for i in range(count - len(id_list)):
    #     id_list.append("")
    return(id_list)

# contact
def indiv_to_corp_contact(value1, corpid, oper, value0): # 人里公司改，公司里人改
    print(' --- contact ---')
    print(value1)
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Corporation.query.get(x)
                    tmp = (my_data.contact)
                    if len(tmp) > 0:
                        tmp = (my_data.contact).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.contact = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Corporation.query.get(x)
            if my_data.contact == "":
                my_data.contact = str(corpid)
            else:
                print(" -- my_data -- " + my_data.contact)
                tmp = (my_data.contact).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.contact = ",".join(tmp)
            print(my_data.contact)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Corporation.query.get(x)
                tmp = (my_data.contact)
                if len(tmp) >0:
                    tmp = (my_data.contact).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.contact = ",".join(tmp)
                        db.session.commit()
        flash("Corp from Individual was updated in Corp table")

def corp_contact_to_indiv(value1, corpid, oper, value0): # 公司里人改，人里公司改
    print(' --- utility contact ---')
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Individual.query.get(x)
                    tmp = (my_data.contact_corp)
                    if len(tmp) > 0:
                        tmp = (my_data.contact_corp).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.contact_corp = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Individual.query.get(x)
            if my_data.contact_corp == "":
                my_data.contact_corp = str(corpid)
            else:
                print(" -- my_data -- " + my_data.contact_corp)
                tmp = (my_data.contact_corp).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.contact_corp = ",".join(tmp)
            print(my_data.contact_corp)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Individual.query.get(x)
                tmp = (my_data.contact_corp)
                if len(tmp) >0:
                    tmp = (my_data.contact_corp).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.contact_corp = ",".join(tmp)
                        db.session.commit()

    flash("Contact from Corp was updated in Individual table")

# director
def indiv_to_corp_director(value1, corpid, oper, value0): # 人里公司改，公司里人改
    print(' --- director ---')
    print(value1)
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Corporation.query.get(x)
                    tmp = (my_data.director)
                    if len(tmp) > 0:
                        tmp = (my_data.director).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.director = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Corporation.query.get(x)
            if my_data.director == "":
                my_data.director = str(corpid)
            else:
                print(" -- my_data -- " + my_data.director)
                tmp = (my_data.director).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.director = ",".join(tmp)
            print(my_data.director)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Corporation.query.get(x)
                tmp = (my_data.director)
                if len(tmp) >0:
                    tmp = (my_data.director).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.director = ",".join(tmp)
                        db.session.commit()
        flash("Director from Individual was updated in Corp table")

def corp_director_to_indiv(value1, corpid, oper, value0): # 公司里人改，人里公司改
    print(' --- director ---')
    print(value1)
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Individual.query.get(x)
                    tmp = (my_data.director_corp)
                    if len(tmp) > 0:
                        tmp = (my_data.director_corp).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.director_corp = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Individual.query.get(x)
            if my_data.director_corp == "":
                my_data.director_corp = str(corpid)
            else:
                print(" -- my_data -- " + my_data.director_corp)
                tmp = (my_data.director_corp).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.director_corp = ",".join(tmp)
            print(my_data.director_corp)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Individual.query.get(x)
                tmp = (my_data.director_corp)
                if len(tmp) >0:
                    tmp = (my_data.director_corp).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.director_corp = ",".join(tmp)
                        db.session.commit()

    flash("Director from Corp was updated in Individual table")

# shareholder
def indiv_to_corp_shareholder(value1, corpid, oper, value0): # 人里公司改，公司里人改
    print(' --- shareholder ---')
    print(value1)
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Corporation.query.get(x)
                    tmp = (my_data.shareholder)
                    if len(tmp) > 0:
                        tmp = (my_data.shareholder).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.shareholder = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Corporation.query.get(x)
            if my_data.shareholder == "":
                my_data.shareholder = str(corpid)
            else:
                print(" -- my_data -- " + my_data.shareholder)
                tmp = (my_data.shareholder).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.shareholder = ",".join(tmp)
            print(my_data.shareholder)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Corporation.query.get(x)
                tmp = (my_data.shareholder)
                if len(tmp) >0:
                    tmp = (my_data.shareholder).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.shareholder = ",".join(tmp)
                        db.session.commit()
    flash("Shareholder from Indiv was updated in Corp table")

def corp_shareholder_to_indiv(value1, corpid, oper, value0): # 公司里人改，人里公司改
    print(' --- shareholder ---')
    print(value1)
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Individual.query.get(x)
                    tmp = (my_data.sharehold_corp)
                    if len(tmp) > 0:
                        tmp = (my_data.sharehold_corp).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.sharehold_corp = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Individual.query.get(x)
            if my_data.sharehold_corp == "":
                my_data.sharehold_corp = str(corpid)
            else:
                print(" -- my_data -- " + my_data.sharehold_corp)
                tmp = (my_data.sharehold_corp).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.sharehold_corp = ",".join(tmp)
            print(my_data.sharehold_corp)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Individual.query.get(x)
                tmp = (my_data.sharehold_corp)
                if len(tmp) >0:
                    tmp = (my_data.sharehold_corp).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.sharehold_corp = ",".join(tmp)
                        db.session.commit()
    flash("Shareholder from Corp was updated in Individual table")

# spouse
def indiv_to_spouse(value1, corpid, oper, value0): # 配偶改
    print(' --- spouse ---')
    print(value1)
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Individual.query.get(x)
                    tmp = (my_data.spouse)
                    if len(tmp) > 0:
                        tmp = (my_data.spouse).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.spouse = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Individual.query.get(x)
            if my_data.spouse == "":
                my_data.spouse = str(corpid)
            else:
                print(" -- my_data -- " + my_data.spouse)
                tmp = (my_data.spouse).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.spouse = ",".join(tmp)
            print(my_data.spouse)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Individual.query.get(x)
                tmp = (my_data.spouse)
                if len(tmp) >0:
                    tmp = (my_data.spouse).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.spouse = ",".join(tmp)
                        db.session.commit()
    flash("Spouse Updated Successfully")

# parents
def parent_to_child(value1, corpid, oper, value0): # 父里子改，子里父改
    print(' --- parents ---')
    print(value1)
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Individual.query.get(x)
                    tmp = (my_data.child)
                    if len(tmp) > 0:
                        tmp = (my_data.child).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.child = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Individual.query.get(x)
            if my_data.child == "":
                my_data.child = str(corpid)
            else:
                print(" -- my_data -- " + my_data.child)
                tmp = (my_data.child).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.child = ",".join(tmp)
            print(my_data.child)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Individual.query.get(x)
                tmp = (my_data.child)
                if len(tmp) >0:
                    tmp = (my_data.child).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.child = ",".join(tmp)
                        db.session.commit()
    flash("parents updated")

# child
def child_to_parent(value1, corpid, oper, value0): # 子里父改，父里子改
    print(' --- child ---')
    print(value1)
    if value0 == "":
        value0 = []
    else:
        value0 = value0.split(',')

    if oper < 2:
        if len(value0) > 0:
            for x in value0:
                if x not in value1:
                    my_data = Individual.query.get(x)
                    tmp = (my_data.parent)
                    if len(tmp) > 0:
                        tmp = (my_data.parent).split(',')
                        if str(corpid) in tmp:
                            tmp.remove(str(corpid))
                            my_data.parent = ",".join(tmp)
                            db.session.commit()

        for x in value1:
            my_data = Individual.query.get(x)
            if my_data.parent == "":
                my_data.parent = str(corpid)
            else:
                print(" -- my_data -- " + my_data.parent)
                tmp = (my_data.parent).split(',')
                if (str(corpid) not in tmp):
                    tmp.append(str(corpid))
                    my_data.parent = ",".join(tmp)
            print(my_data.parent)
            db.session.commit()

    elif oper == 2:
        if len(value0) > 0:
            for x in value0:
                my_data = Individual.query.get(x)
                tmp = (my_data.parent)
                if len(tmp) >0:
                    tmp = (my_data.parent).split(',')
                    if str(corpid) in tmp:
                        tmp.remove(str(corpid))
                        my_data.parent = ",".join(tmp)
                        db.session.commit()
    flash("Child Updated Successfully")

# get Index array
def get_index_index(type, id_list, dropdown_list): # 由ID字串获取下拉菜单index字串
    index_list = []
    tmp0 = []
    for x in dropdown_list:
        if type == 'Corporation':
            tmp0.append(str(x.indiv_id))
        elif type == 'Individual':
            tmp0.append(str(x.corp_id))

    for x in id_list:
        tmp1 = []
        if (len(x)>0):
            x = x.split(',')
            for y in x:
                if len(y)>0:
                    if tmp0.count(y)>0:
                        tmp1.append(tmp0.index(y))
        index_list.append(tmp1)
    return index_list