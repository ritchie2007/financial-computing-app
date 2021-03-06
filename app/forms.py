from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=3,max=20,message='length 3-20'), DataRequired(message='can not be empty')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    ''' add new user '''
    username = StringField(
        'Username', 
        validators=[
            Length(min=3,max=20,message='length 3-20'), 
            DataRequired(message='can not be empty')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    password_repeat = PasswordField(
        'Repeat Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists. Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already exists. Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    about_me = TextAreaField(
        'About me',
        validators=[Length(min=0, max=140)]
    )
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')

class WebNavForm(FlaskForm):
    website = StringField(
        'Website',
        validators=[DataRequired()]
    )
    submit = SubmitField('Go')