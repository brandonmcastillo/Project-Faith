import os
from flask import Flask, g, request
from flask import render_template, flash, redirect, url_for, session, escape, request
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.urls import url_parse
import models
import forms
from flask_assets import Environment, Bundle
import json

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

def main():
    return render_template('main.html')

@app.route('/articles')
@login_required
def articles():
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
@login_required
def thispost(postid=None):
    if postid != None and request.method == 'GET':
        print('in if')
        post = models.Post.select().where(models.Post.id == postid).get()
        user = g.user._get_current_object()
        replies = models.Reply.select().where(models.Reply.post_id == postid)
        replyid = models.Reply.select().where(models.Reply.id)
        replythread = models.ReplyThread.select().where(models.ReplyThread.reply_id == replyid)
        return render_template('postpage.html', post=post, replies=replies, replyid=replyid, replythread=replythread)
    else:
        return('error')    

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
        return redirect(url_for('thispost', postid=post.id))
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
        return redirect(url_for('thispost', postid=post.id))
    form.category.default = post.category
    form.process()
    return render_template('edit-post.html', form=form, post=post)

@app.route('/delete-post/<postid>', methods=['GET','DELETE'])
@login_required
def delete_post(postid=None):
    if postid != None:
        user = models.User.get(current_user.id)
        delete_post = models.Post.delete().where(models.Post.id == postid)
        delete_post.execute()
        return redirect(url_for('profile', username=user.username))
    return redirect(url_for('edit-post', postid=postid))

@app.route('/post/<postid>/reply', methods=['GET','POST'])
@login_required
def reply_post(postid=None):
    form = forms.CreateReplyForm()
    if postid != None and request.method == 'POST':
            user = g.user._get_current_object()
            post = models.Post.select().where(models.Post.id == postid).get()
            models.Reply.create(
                user=user.id, 
                post=post.id, 
                content=form.content.data)
            content = models.Reply.get(models.Reply.content == form.content.data)
            return redirect(url_for('thispost', user=user, postid=post.id))
    return render_template('reply-form.html', form=form, postid=postid)

@app.route('/post/<postid>/edit-reply/<replyid>', methods=['GET', 'POST'])
@login_required
def edit_reply_post(postid=None, replyid=None):
    form = forms.EditReplyForm()
    reply = models.Reply.select().where(models.Reply.id == replyid).get()
    post = models.Post.select().where(models.Post.id == postid).get()
    user = g.user._get_current_object()
    if form.validate_on_submit():
        reply.content = form.content.data
        reply.save() 
        return redirect(url_for('thispost',  user=user, postid=post.id))
    return render_template('edit-comment.html', form=form, postid=postid, replies=reply)

@app.route('/post/<postid>/delete-reply/<replyid>', methods=['GET', 'DELETE'])
@login_required
def delete_reply_post(postid=None, replyid=None):
    if replyid != None:
        delete_reply = models.Reply.delete().where(models.Reply.id == replyid)
        post = models.Post.select().where(models.Post.id == postid).get()
        delete_reply.execute()
        return redirect(url_for('thispost',  postid=post.id))

@app.route('/post/<postid>/reply/<replyid>/reply', methods=['GET','POST'])
@login_required
def create_reply_to_reply(postid=None, replyid=None):
    form = forms.CreateReplyForm()
    reply = models.Reply.select().where(models.Reply.id == replyid).get()
    if postid != None and reply != None and request.method == 'POST':
            user = g.user._get_current_object()
            reply = models.Reply.select().where(models.Reply.id == replyid).get()
            post = models.Post.select().where(models.Post.id == postid).get()
            models.ReplyThread.create(
                user=user.id, 
                reply=reply.id, 
                content=form.content.data)
            return redirect(url_for('thispost', postid=post.id))
    return render_template('reply-form.html', form=form, postid=postid)

@app.route('/post/<postid>/reply/<replyid>/edit-reply/<subcommentid>', methods=['GET','POST'])
@login_required
def edit_reply_to_reply(postid=None, replyid=None, subcommentid=None):
    form = forms.EditReplyForm()
    subcommentid = models.ReplyThread.select().where(models.ReplyThread.id == subcommentid).get()
    reply = models.Reply.select().where(models.Reply.id == replyid).get()
    post = models.Post.select().where(models.Post.id == postid).get()
    user = g.user._get_current_object()
    if form.validate_on_submit():
        subcommentid.content = form.content.data
        subcommentid.save() 
        return redirect(url_for('thispost',  user=user, postid=post.id))
    return render_template('edit-subcomment.html', form=form, postid=postid, replies=reply, subcommentid=subcommentid)

@app.route('/post/<postid>/reply/<replyid>/delete-reply/<subcommentid>', methods=['GET', 'DELETE'])
@login_required
def delete_reply_to_reply(postid=None, replyid=None, subcommentid=None):
    if subcommentid != None:
        delete_this_reply = models.ReplyThread.delete().where(models.ReplyThread.id == subcommentid)
        post = models.Post.select().where(models.Post.id == postid).get()
        reply = models.Reply.select().where(models.Reply.id == replyid).get()
        delete_this_reply.execute()
        return redirect(url_for('thispost',  postid=post.id))

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