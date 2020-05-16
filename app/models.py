from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
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
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Dailyentry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(12))
    staff = db.Column(db.String(80))
    starttime = db.Column(db.String(10))
    calhr = db.Column(db.Float)
    workhr = db.Column(db.Float)
    comment = db.Column(db.String(200))
    taskname = db.Column(db.String(100))
    tasktype = db.Column(db.String(100))
    taskcode = db.Column(db.Integer)
    corp1 = db.Column(db.String(100))
    corp2 = db.Column(db.String(100))
    corp3 = db.Column(db.String(100))
    corp4 = db.Column(db.String(100))
    taskcontent = db.Column(db.Text)

    def __init__(
        self,
        date,
        staff,
        starttime,
        calhr,
        workhr,
        comment,
        taskname,
        tasktype,
        taskcode,
        corp1,
        corp2,
        corp3,
        corp4,
        taskcontent
    ):
        self.date = date
        self.staff = staff
        self.starttime = starttime
        self.calhr = calhr
        self.workhr = workhr
        self.comment = comment
        self.taskname = taskname
        self.tasktype = tasktype
        self.taskcode = taskcode
        self.corp1 = corp1
        self.corp2 = corp2
        self.corp3 = corp3
        self.corp4 = corp4
        self.taskcontent = taskcontent
