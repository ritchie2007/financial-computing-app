from datetime import datetime
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, WebNavForm
from app.models import User, Data_table

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

@app.route(
    '/timesheet'
)
def timesheet():
    return render_template(
        'timesheet.html',
        title='timesheet'
    )

@app.route(
    '/temp'
)
def temp():
    return render_template(
        'temp.html',
        title='temp'
    )

# **** following is to try Data table CRUD functions ******
# This is the data_table root on all our employee data
@app.route(
    '/data_table'
)
def data_table():
    all_data = Data_table.query.all() # Data_table is defined in models.py
    return render_template(
        'data_table.html',
        employees = all_data,
        title = 'data_table'
    )
#this route is for inserting data to mysql database via html forms
@app.route('/data_table/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
 
        my_data = Data_table(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        flash("Employee Inserted Successfully")
        return redirect(url_for('data_table'))
#this is our update route where we are going to update our employee
@app.route('/data_table/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data_table.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('data_table'))
#This route is for deleting our employee
@app.route('/data_table/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data_table.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('data_table'))
 