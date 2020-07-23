from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(userid):
    ''' get user info'''
    return User.query.get(int(userid))

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
    startdate = db.Column(db.String(10))
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
    timestamp = db.Column(db.Integer)
    avgtime = db.Column(db.String(10))
    jobid1 = db.Column(db.Integer)
    jobid2 = db.Column(db.Integer)
    jobid3 = db.Column(db.Integer)
    jobid4 = db.Column(db.Integer)
    starttime = db.Column(db.String(5))
    serialno = db.Column(db.String(20))
    def __init__(self, startdate, calhour, adjhour, adjmin, workhour, taskname, taskcontent, tasktype, \
             corp1, corp2, corp3, corp4, staff, timestamp, avgtime, jobid1, jobid2, jobid3, jobid4, starttime, serialno):
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
        self.timestamp = timestamp
        self.avgtime = avgtime
        self.jobid1 = jobid1
        self.jobid2 = jobid2
        self.jobid3 = jobid3
        self.jobid4 = jobid4
        self.starttime = starttime
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
    def __init__(self, client, jobtype, periodend, details, nextstartdate, nextenddate, \
        status, priority, recurrence, jobowner, serialno, worktime, renewperiod, renewstartdate, \
        renewenddate):
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
    name = db.Column(db.String(80))
    date = db.Column(db.String(15))
    job = db.Column(db.String(80))
    calendar_hour = db.Column(db.String(10))
    adj_hour = db.Column(db.String(5))
    adj_min = db.Column(db.String(5))
    work_hour = db.Column(db.String(12))
    timestamp = db.Column(db.Integer)
    serialno = db.Column(db.String(20))
    def __init__(self, name, date, job, calendar_hour, adj_hour, adj_min, work_hour, timestamp, serialno):
        self.name = name
        self.date = date
        self.job = job
        self.calendar_hour = calendar_hour
        self.adj_hour = adj_hour
        self.adj_min = adj_min
        self.work_hour = work_hour
        self.timestamp = timestamp
        self.serialno = serialno

class CorprationReport(db.Model):
    __tablename__ = "corpration_report"
    id = db.Column(db.Integer, primary_key=True)
    corp = db.Column(db.String(100))
    date = db.Column(db.String(20))
    task_name = db.Column(db.String(80))
    task_type = db.Column(db.String(80))
    task_content = db.Column(db.Text)
    work_hour = db.Column(db.String(10))
    timestamp = db.Column(db.Integer)
    jobid = db.Column(db.Integer)
    serialno = db.Column(db.String(20))
    def __init__(self, corp, date, task_name, task_type, task_content, work_hour, timestamp, jobid, serialno):
        self.corp = corp
        self.date = date
        self.task_name = task_name
        self.task_type = task_type
        self.task_content = task_content
        self.work_hour = work_hour
        self.timestamp = timestamp
        self.jobid = jobid
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

class Corporation(db.Model):
    ''' corporation detail information'''
    __tablename__ = 'tbl_Corporation'
    corp_id = db.Column(db.Integer, primary_key=True)
    corp1 = db.Column(db.String(10))
    corp2 = db.Column(db.String(150))
    corp3 = db.Column(db.String(50))
    corp4 = db.Column(db.String(50))
    corp5 = db.Column(db.String(20))
    corp6 = db.Column(db.String(20))
    corp7 = db.Column(db.String(20))
    corp8 = db.Column(db.String(20))
    corp9 = db.Column(db.String(20))
    corp10 = db.Column(db.String(20))
    corp11 = db.Column(db.String(10))
    corp12 = db.Column(db.String(10))
    corp13 = db.Column(db.String(10))
    corp14 = db.Column(db.String(10))
    corp15 = db.Column(db.String(10))
    corp16 = db.Column(db.String(150))
    corp17 = db.Column(db.String(150))
    corp18 = db.Column(db.String(100))
    corp19 = db.Column(db.String(100))
    corp20 = db.Column(db.String(20))
    corp21 = db.Column(db.String(20))
    corp22 = db.Column(db.String(100))
    corp23 = db.Column(db.String(200))
    corp24 = db.Column(db.String(150))
    corp25 = db.Column(db.String(20))
    corp26 = db.Column(db.String(20))
    corp27 = db.Column(db.String(20))
    corp28 = db.Column(db.String(20))
    corp29 = db.Column(db.String(150))
    corp30 = db.Column(db.String(20))
    corp31 = db.Column(db.String(150))
    corp32 = db.Column(db.String(150))
    corp33 = db.Column(db.String(150))
    corp34 = db.Column(db.String(20))
    corp35 = db.Column(db.String(150))
    corp36 = db.Column(db.String(50))
    corp37 = db.Column(db.String(150))
    corp38 = db.Column(db.String(20))
    corp39 = db.Column(db.String(80))
    corp40 = db.Column(db.String(20))
    corp41 = db.Column(db.String(80))
    corp42 = db.Column(db.String(50))
    corp43 = db.Column(db.String(150))
    corp44 = db.Column(db.String(150))
    corp45 = db.Column(db.String(150))
    corp46 = db.Column(db.String(80))
    corp47 = db.Column(db.String(200))
    corp48 = db.Column(db.String(200))
    corp49 = db.Column(db.String(120))
    corp50 = db.Column(db.String(120))
    corp51 = db.Column(db.String(120))
    corp52 = db.Column(db.String(80))
    corp53 = db.Column(db.String(30))
    corp54 = db.Column(db.String(80))
    corp55 = db.Column(db.String(30))
    corp56 = db.Column(db.String(200))
    corp57 = db.Column(db.String(120))
    corp58 = db.Column(db.String(150))
    contact = db.Column(db.String(40))
    director = db.Column(db.String(40))
    shareholder = db.Column(db.String(40))
    task = db.Column(db.Integer)
    recent_update = db.Column(db.String(50))
    contact_position = db.Column(db.String(200))
    shareholder_info = db.Column(db.String(400))
    timestamp = db.Column(db.String(26))

    def __init__(self,corp1,corp2,corp3,corp4,corp5,corp6,corp7,corp8,corp9,corp10,corp11,corp12,corp13,corp14,corp15,corp16,corp17,corp18,corp19,corp20,corp21,corp22,corp23,corp24,corp25,corp26,corp27,corp28,corp29,corp30,corp31,corp32,corp33,corp34,corp35,corp36,corp37,corp38,corp39,corp40,corp41,corp42,corp43,corp44,corp45,corp46,corp47,corp48,corp49,corp50,corp51,corp52,corp53,corp54,corp55,corp56,corp57,corp58,contact,director,shareholder,task,recent_update,contact_position,shareholder_info,timestamp):
        self.corp1 = corp1
        self.corp2 = corp2
        self.corp3 = corp3
        self.corp4 = corp4
        self.corp5 = corp5
        self.corp6 = corp6
        self.corp7 = corp7
        self.corp8 = corp8
        self.corp9 = corp9
        self.corp10 = corp10
        self.corp11 = corp11
        self.corp12 = corp12
        self.corp13 = corp13
        self.corp14 = corp14
        self.corp15 = corp15
        self.corp16 = corp16
        self.corp17 = corp17
        self.corp18 = corp18
        self.corp19 = corp19
        self.corp20 = corp20
        self.corp21 = corp21
        self.corp22 = corp22
        self.corp23 = corp23
        self.corp24 = corp24
        self.corp25 = corp25
        self.corp26 = corp26
        self.corp27 = corp27
        self.corp28 = corp28
        self.corp29 = corp29
        self.corp30 = corp30
        self.corp31 = corp31
        self.corp32 = corp32
        self.corp33 = corp33
        self.corp34 = corp34
        self.corp35 = corp35
        self.corp36 = corp36
        self.corp37 = corp37
        self.corp38 = corp38
        self.corp39 = corp39
        self.corp40 = corp40
        self.corp41 = corp41
        self.corp42 = corp42
        self.corp43 = corp43
        self.corp44 = corp44
        self.corp45 = corp45
        self.corp46 = corp46
        self.corp47 = corp47
        self.corp48 = corp48
        self.corp49 = corp49
        self.corp50 = corp50
        self.corp51 = corp51
        self.corp52 = corp52
        self.corp53 = corp53
        self.corp54 = corp54
        self.corp55 = corp55
        self.corp56 = corp56
        self.corp57 = corp57
        self.contact = contact
        self.director = director
        self.shareholder = shareholder
        self.task = task
        self.recent_update = recent_update
        self.contact_position = contact_position
        self.shareholder_info = shareholder_info
        self.timestamp = timestamp

class Individual(db.Model):
    ''' Indivuduals detail information '''
    __tablename__ = 'tbl_Individual'
    indiv_id = db.Column(db.Integer, primary_key=True)
    sin = db.Column(db.Integer)
    prefix = db.Column(db.String(10))
    last_name = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    other_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone1 = db.Column(db.String(15))
    phone2 = db.Column(db.String(15))
    address1 = db.Column(db.String(150))
    address2 = db.Column(db.String(150))
    mail_address = db.Column(db.String(150))
    wechat = db.Column(db.String(150))
    cra_sole_proprietor = db.Column(db.String(100))
    cra_hst_report  = db.Column(db.String(100))
    cra_payroll  = db.Column(db.String(100))
    cra_withhold_tax  = db.Column(db.String(100))
    cra_wsib = db.Column(db.String(50))
    cra_other = db.Column(db.String(100))
    oversea_asset_t1135 = db.Column(db.String(200))
    oversea_corp_t1134 = db.Column(db.String(200))
    tslip = db.Column(db.String(50))
    tax_personal_info = db.Column(db.String(200))
    specific_info = db.Column(db.String(200))
    engage_account = db.Column(db.String(200))
    engage_leading = db.Column(db.String(200))
    note = db.Column(db.String(200))
    contact_corp = db.Column(db.String(30))
    director_corp = db.Column(db.String(30))
    sharehold_corp = db.Column(db.String(30))
    spouse = db.Column(db.String(20))
    parent = db.Column(db.String(40))
    child = db.Column(db.String(40))
    timestamp = db.Column(db.String(26))
    def __init__(self,sin,prefix,last_name,first_name,other_name,email,phone1,phone2,address1,address2,mail_address,
        wechat,cra_sole_proprietor,cra_hst_report,cra_payroll,cra_withhold_tax,cra_wsib,cra_other,oversea_asset_t1135,
        oversea_corp_t1134,tslip,tax_personal_info,specific_info,engage_account,engage_leading,note,
        contact_corp,director_corp,sharehold_corp,spouse,parent,child,timestamp):

        self.sin = sin
        self.prefix = prefix
        self.last_name = last_name
        self.first_name = first_name
        self.other_name = other_name
        self.email = email
        self.phone1 = phone1
        self.phone2 = phone2
        self.address1 = address1
        self.address2 = address2
        self.mail_address = mail_address
        self.wechat = wechat
        self.cra_sole_proprietor = cra_sole_proprietor
        self.cra_hst_report = cra_hst_report
        self.cra_payroll = cra_payroll
        self.cra_withhold_tax = cra_withhold_tax
        self.cra_wsib = cra_wsib
        self.cra_other = cra_other
        self.oversea_asset_t1135 = oversea_asset_t1135
        self.oversea_corp_t1134 = oversea_corp_t1134
        self.tslip = tslip
        self.tax_personal_info = tax_personal_info
        self.specific_info = specific_info
        self.engage_account = engage_account
        self.engage_leading = engage_leading
        self.note = note
        self.contact_corp = contact_corp
        self.director_corp = director_corp
        self.sharehold_corp = sharehold_corp
        self.spouse = spouse
        self.parent = parent
        self.child = child
        self.timestamp = timestamp

class Directors(db.Model):
    ''' directors linked to corporation'''
    __tablename__ = 'tbl_Directors'
    director_id = db.Column(db.String(15), primary_key=True)
    corp_no = db.Column(db.String(20))
    corp_director_no = db.Column(db.Integer)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    sin = db.Column(db.String(20))
    address = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Shareholders(db.Model):
    ''' shareholders linked to corporation'''
    __tablename__ = 'tbl_Shareholders'
    shareholder_id = db.Column(db.String(15), primary_key=True)
    corp_no = db.Column(db.String(20))
    corp_share_no = db.Column(db.Integer)
    shares = db.Column(db.String(80))
    shares_percent = db.Column(db.String(10))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    sin = db.Column(db.String(20))
    address = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
