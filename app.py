import os
from flask import Flask, g, request
from flask import render_template, flash, redirect, url_for, session, escape
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
import models
import forms


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')
app.secret_key = 'asdfghjkl'

DEBUG = True
PORT = 8000

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()
  g.user = current_user

@app.after_request
def after_request(response):
  g.db.close()
  return response



@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/articles')
def about():
    return render_template('articles.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Email or password not found.  Please sign up!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                ## creates session
                login_user(user)
                flash("You successfully logged in", "success")
                return redirect(url_for('profile', username=user.username))
            else:
                flash("Your email or password doesn't match", "error")
    return render_template('login.html', form=form)

@app.route('/signup', methods=('GET', 'POST'))
def register():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        filename = images.save(request.files['profile_image'])
        url = images.url(filename)

        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            location=form.location.data,
        )
        
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        name = user.username
        flash('Thank you for signing up', 'success')
        return redirect(url_for('profile', username=name))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Initialize models when running on localhost
if __name__ == '__main__':
    models.initialize()

app.run(debug=DEBUG, port=PORT)