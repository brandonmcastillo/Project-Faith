import os
from flask import Flask, g, request
from flask import render_template, flash, redirect, url_for, session, escape, request
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
import models
import forms
from flask_assets import Environment, Bundle
from newsapi.newsapi_client import NewsApiClient
import json
import requests

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'kattdakattdakatt'
assets = Environment(app)
assets.init_app(app)

DEBUG = True
PORT = 8000

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try: 
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

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
@login_required
def main():
    return render_template('main.html')

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
                return redirect(url_for('main'))
            else:
                flash("Your email or password doesn't match", "error")
    return render_template('login.html', form=form)

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        models.User.create_user(
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )  
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        name = user.username
        flash('Welcome back to Faith', 'success')
        return redirect(url_for('main'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/community', methods=['GET'])
@app.route('/community/<postid>', methods=['GET', 'POST'])
@login_required
def posts(postid=None):
    if postid == None:
        posts = models.Post.select().limit(10)
        return render_template('community.html', posts=posts)
    return render_template('community.html')

@app.route('/post/<postid>', methods=['GET','POST'])
def thispost(postid=None):
    if postid != None:
        post = models.Post.select().where(models.Post.id == postid).get()
        return render_template('postpage.html', post=post)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = forms.CreatePostForm()
    user = g.user._get_current_object()
    if request.method == 'POST':
        models.Post.create(
            title = form.title.data,
            category = form.category.data,
            content = form.content.data,
            user = g.user._get_current_object()
        )
        post = models.Post.get(models.Post.title == form.title.data)
        flash('You have created a post! We hope you hear from others soon!', 'success')
        return redirect(url_for('posts'))
    else:
        return render_template('create-post.html', form=form, user=user)

@app.route('/edit-post/<postid>', methods=['GET', 'POST'])
@login_required
def edit_post(postid = None):
    post = models.Post.select().where(models.Post.id == postid).get()
    form = forms.EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.content = form.content.data
        post.save()
        return redirect(url_for('posts'))
    form.category.default = post.category
    form.process()
    return render_template('edit-post.html', form=form, post=post)

@app.route('/delete-post/<postid>', methods=['GET','DELETE'])
@login_required
def delete_post(postid=None):
    if postid != None:
        post = models.Post.select().where(models.Post.id == postid).get()
        delete_post = post.delete()
        delete_post.execute()
        return redirect(url_for('posts'))
    return redirect(url_for('edit-post', postid=postid))


@app.route('/post/<postid>/reply', methods=['GET','POST'])
def reply_post(postid=None):
    form = forms.CreateReplyForm()
    user = g.user._get_current_object()
    post = models.Post.select().where(models.Post.id == postid).get()
    if postid != None:
        if form.validate_on_submit():
            post.content = form.content.data
            post.save()
            models.Reply.create(user=user.id, post=post.id, content=post.content)
            return render_template('postpage.html', post=post)
    return render_template('reply-form.html', form=form, postid=postid)





@app.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username=None):
    if username != None and request.method == 'GET':
        user = models.User.select().where(models.User.username==username).get()
        posts = models.Post.select().where(models.Post.user == user.id)
        Owner = user.alias()
        return render_template('profile.html', user=user, posts=posts)
    return redirect(url_for('index'))

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = models.User.get(current_user.id)
    form = forms.EditUserForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data
        user.save()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile', username=user.username))
    return render_template('edit-profile.html', form=form, user=user)

@app.route('/https://newsapi.org/v2/top-headlines?sources=medical-news-today&apiKey=77dbc22b934c410dad8e84f2c444cffc', methods=['GET'])
@login_required
def articles():
    newsapi = NewsApiClient(api_key='77dbc22b934c410dad8e84f2c444cffc')
    top_headlines = newsapi.get_top_headlines(sources='medical-news-today',
    )
    print(top_headlines['articles'])
    return render_template('articles.html', top_headlines=top_headlines, newsapi=newsapi)

    





if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
        username='brandon',
        name="brandon",
        email="brandon@gmail.com",
        password='password'
        )
    except ValueError:
        pass

app.run(debug=DEBUG, port=PORT)