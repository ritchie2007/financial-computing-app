from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id): # load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Data_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

class activity_code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    def __init__(self, name):
        self.name = name

class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startdate = db.Column(db.String(20))
    calhour = db.Column(db.String(10))
    adjhour = db.Column(db.String(4))
    adjmin = db.Column(db.String(4))
    workhour = db.Column(db.String(10))
    taskname = db.Column(db.String(80))
    taskcontent = db.Column(db.Text)
    tasktype = db.Column(db.String(80))
    corp1 = db.Column(db.String(100))
    corp2 = db.Column(db.String(100))
    corp3 = db.Column(db.String(100))
    corp4 = db.Column(db.String(100))
    staff = db.Column(db.String(50))
    serialno = db.Column(db.String(20))
    def __init__(self,
        startdate,
        calhour,
        adjhour,
        adjmin,
        workhour,
        taskname,
        taskcontent,
        tasktype,
        corp1,
        corp2,
        corp3,
        corp4,
        staff,
        serialno):
        self.startdate = startdate
        self.calhour = calhour
        self.adjhour = adjhour
        self.adjmin = adjmin
        self.workhour = workhour
        self.taskname = taskname
        self.taskcontent = taskcontent
        self.tasktype = tasktype
        self.corp1 = corp1
        self.corp2 = corp2
        self.corp3 = corp3
        self.corp4 = corp4
        self.staff = staff
        self.serialno = serialno

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100))
    jobtype = db.Column(db.String(20))
    periodend = db.Column(db.String(10))
    details = db.Column(db.String(100))
    nextstartdate = db.Column(db.String(10))
    nextenddate = db.Column(db.String(10))
    status = db.Column(db.String(12))
    priority = db.Column(db.String(10))
    recurrence = db.Column(db.String(10))
    jobowner = db.Column(db.String(20))
    serialno = db.Column(db.Float())
    worktime = db.Column(db.String(10))
    renewperiod = db.Column(db.String(10))
    renewstartdate = db.Column(db.String(10))
    renewenddate = db.Column(db.String(10))
    
    def __init__(self, client, jobtype, periodend, details, nextstartdate, nextenddate, 
    status, priority, recurrence, jobowner, serialno, worktime, renewperiod, renewstartdate, renewenddate):
        self.client = client
        self.jobtype = jobtype
        self.periodend = periodend
        self.details = details
        self.nextstartdate = nextstartdate
        self.nextenddate = nextenddate
        self.status = status
        self.priority = priority
        self.recurrence = recurrence
        self.jobowner = jobowner
        self.serialno = serialno
        self.worktime = worktime
        self.renewperiod = renewperiod
        self.renewstartdate = renewstartdate
        self.renewenddate = renewenddate

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    job = db.Column(db.String(100))
    calendar_hour = db.Column(db.String(12))
    adj_hour = db.Column(db.String(12))
    work_hour = db.Column(db.String(12))
    serialno = db.Column(db.String(12))
    def __init__(self, name, job, calendar_hour, adj_hour, work_hour, serialno):
        self.name = name
        self.job = job
        self.calendar_hour = calendar_hour
        self.adj_hour = adj_hour
        self.work_hour = work_hour
        self.serialno = serialno

class Corpration_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(12))
    corp = db.Column(db.String(100))
    task_name = db.Column(db.String(100))
    task_content = db.Column(db.Text)
    task_type = db.Column(db.String(100))
    work_hour = db.Column(db.String(12))
    serialno = db.Column(db.String(12))
    def __init__(self, date, corp, task_name, task_content, task_type, work_hour, serialno):
        self.date = date
        self.corp = corp
        self.task_name = task_name
        self.task_content = task_content
        self.task_type = task_type
        self.work_hour = work_hour
        self.serialno = serialno

class TimesheetTempData(db.Model):
    __tablename__ = 'timesheettempdata'
    t0 = db.Column(db.String(15), primary_key=True)
    t1 = db.Column(db.String(20))
    t2 = db.Column(db.String(10))
    t3 = db.Column(db.String(4))
    t4 = db.Column(db.String(4))
    t5 = db.Column(db.String(10))
    t6 = db.Column(db.String(100))
    t7 = db.Column(db.String(200))
    t8 = db.Column(db.String(80))
    t9 = db.Column(db.String(100))
    t10 = db.Column(db.String(100))
    t11 = db.Column(db.String(100))
    t12 = db.Column(db.String(100))
    t13 = db.Column(db.Integer)

class Mulform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    def __init__(self, name):
        self.name = name
