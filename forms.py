from flask_wtf import FlaskForm as Form
from models import User, Post, Reply, ReplyThread
from wtforms import StringField, PasswordField, TextAreaField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Regexp, ValidationError, Length, EqualTo, Email

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with this username already exists! Try again")

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with this email already exists! Try again!")

class SignUpForm(Form):
    username = StringField(
        'Username:',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should only be one word, Letters"
                         " numbers and underscores are only allowed.")),
            name_exists
        ])
    name = StringField(
        'Name:',
        validators=[
            DataRequired(),
        ])
    email = StringField(
        'Email:',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired(),
            Length(min=3),
            EqualTo('password2', message='Passwords must match. Try again.')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()
        ])
class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
        )
class EditUserForm(Form):
    name = StringField('Name')
    email = StringField('Email')
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired(),
            Length(min=3),
            EqualTo('password2', message='Passwords must be identical. Try again.')
        ])
    password2 = PasswordField(
        'Confirm Your Password',
        validators=[DataRequired()
        ])

class CreatePostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Anxiety', 'Anxiety'),('Mood', 'Mood'),('Eating Disorder', 'Eating Disorder'),('Substance Abuse', 'Substance Abuse'), ('Schizophrenia', 'Schizophrenia'), ('Dementia', 'Dementia'), ('Phobia', 'Phobia'), ('PTSD', 'PTSD'), ('OCD', 'OCD'), ('General Health', 'General Health')])
    content = StringField('content', validators=[DataRequired()])

class EditPostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Anxiety', 'Anxiety'),('Mood', 'Mood'),('Eating Disorder', 'Eating Disorder'),('Substance Abuse', 'Substance Abuse'), ('Schizophrenia', 'Schizophrenia'), ('Dementia', 'Dementia'), ('Phobia', 'Phobia'), ('PTSD', 'PTSD'), ('OCD', 'OCD'), ('General Health', 'General Health')])
    content = TextAreaField('content', validators=[DataRequired()])

class CreateReplyForm(Form):
    content = StringField('content', validators=[DataRequired()])

class EditReplyForm(Form):
    content = StringField('content', validators=[DataRequired()])