from flask.ext.wtf  import Form
from flask import flash
from wtforms import TextField, BooleanField, PasswordField, StringField, PasswordField,SubmitField
from wtforms.validators import Required, Email, EqualTo, Length, Email, Regexp, ValidationError
from app.models import User


class LoginForm(Form):
    email = TextField('Email Address', [Email(),
                        Required(message='Email authentication required')])
    password = PasswordField('Password',[Required(message='Inpust your password')])
    remember_me =BooleanField('Remember password')
    submit = SubmitField('Log in')

class Signup(Form):
    name = StringField('Enter your name', validators=[Required(), Length(1,64),
                                                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                         'Name should contain only leters, numbers, dots or underscores')]) 
    email = StringField('Enter email',validators=[Required(), Email(), Length(1,64)])
    password = PasswordField('password', validators= [Required(),EqualTo('password2',message='The passwords are not similar match')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Sign Up')

    def  validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Name is already in use, pick a unique one')

    def  validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email already exists')
        

class ChangePassword(Form):
    old_password = PasswordField('Input old Password', validators=[Required()])
    password = PasswordField('New Password', validators=[Required(),
                              EqualTo('Password2', message= 'Passwords do not match.')])
    password2 = PasswordField('Confirm New password', validators=[Required()])
    submit = SubmitField('Update Password')

class PasswordResetRequest(Form):
    email =StringField('Email', validators=[Required(), Length(1, 64),Email()])
    submit = SubmitField('Reset Password')


class PasswordReset(Form):
    email = StringField('Email', validators=[Required(), Length])    
    password = PasswordField('New password', validators=[Required(),
                EqualTo('password2', message='Enter similar passwords')])
    password2 = PasswordField('Confirm New passsword', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Email Address is Invalid')



class ChangeEmail(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64), Email()])
    password =PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use.')
    