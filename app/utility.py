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
def indiv_to_corp_contact(name, id):
    print(' --- contact ---')
    print(name)
    for i in name:
        my_data = Corporation.query.get(i)
        if my_data.corp59 == "":
            my_data.corp59 = str(id)
        else:
            print(" -- my_data -- " + my_data.corp59)
            tmp = (my_data.corp59).split(',')
            if (str(id) not in tmp):
                tmp.append(str(id))
                my_data.corp59 = ",".join(tmp)
        print(my_data.corp59)
        db.session.commit()
        flash("Contact Updated Successfully")

# director
def indiv_to_corp_director(name,id):
    print(' --- director ---')
    print(name)
    for i in name:
        my_data = Corporation.query.get(i)
        if my_data.corp60 == "":
            my_data.corp60 = str(id)
        else:
            print(" -- my_data -- " + my_data.corp60)
            tmp = (my_data.corp60).split(',')
            if (str(id) not in tmp):
                tmp.append(str(id))
                my_data.corp60 = ",".join(tmp)
        print(my_data.corp60)
        db.session.commit()
        flash("Director Updated Successfully")

# shareholder
def indiv_to_corp_shareholder(name,id):
    print(' --- shareholder ---')
    print(name)
    for i in name:
        my_data = Corporation.query.get(i)
        if my_data.corp61 == "":
            my_data.corp61 = str(id)
        else:
            print(" -- my_data -- " + my_data.corp61)
            tmp = (my_data.corp61).split(',')
            if (str(id) not in tmp):
                tmp.append(str(id))
                my_data.corp61 = ",".join(tmp)
        print(my_data.corp61)
        db.session.commit()
        flash("Director Updated Successfully")

# spouse
def indiv_to_spouse(name,id):
    print(' --- spouse ---')
    print(name)
    for i in name:
        my_data = Individual.query.get(i)
        if my_data.spouse == "":
            my_data.spouse = str(id)
        else:
            print(" -- my_data -- " + my_data.spouse)
            tmp = (my_data.spouse).split(',')
            if (str(id) not in tmp):
                tmp.append(str(id))
                my_data.spouse = ",".join(tmp)
        print(my_data.spouse)
        db.session.commit()
        flash("Shareholder Updated Successfully")

# parents
def indiv_to_parent(name,id):
    print(' --- parents ---')
    print(name)
    for i in name:
        my_data = Individual.query.get(i)
        if my_data.child == "":
            my_data.child = str(id)
        else:
            print(" -- my_data -- " + my_data.child)
            tmp = (my_data.child).split(',')
            if (str(id) not in tmp):
                tmp.append(str(id))
                my_data.child = ",".join(tmp)
        print(my_data.child)
        db.session.commit()
        flash("Parent Updated Successfully")

# child
def indiv_to_child(name,id):
    print(' --- child ---')
    print(name)
    for i in name:
        my_data = Individual.query.get(i)
        if my_data.parent == "":
            my_data.parent = str(id)
        else:
            print(" -- my_data -- " + my_data.parent)
            tmp = (my_data.parent).split(',')
            if (str(id) not in tmp):
                tmp.append(str(id))
                my_data.parent = ",".join(tmp)
        print(my_data.parent)
        db.session.commit()
        flash("Child Updated Successfully")
