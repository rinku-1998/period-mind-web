from app import db, login, upload
from app.main.forms import LoginForm, PostForm, RegisterForm, EditProfileForm
from app.main.models import Account, Post, Category

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.main import bp

from datetime import datetime
import hashlib

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # Load with SQL syntax
    syntax = 'SELECT account.username, post.* FROM post JOIN account ON account.accountID == post.accountID ORDER BY post.postTime desc'
    result = db.session.execute(syntax)
    for r in result:
        print(r)
    # Load with DB-ORM
    # posts = Post.query.join(Account).filter(Account.accountID == Post.accountID).all()
    # posts = Post.query.join(Account, (Account.accountID == Post.accountID)).all()
    # names = [row[0] for row in result]
    # print (names)
    
    # for post in posts:
    #     print(vars(post))
    # return render_template('index.html', posts=posts)
    return 'ok'

@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        hashed_filename = None #Default for no file uploaded
        if not form.postImage.data.filename == '':
            m = hashlib.md5()
            current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            file_type = form.postImage.data.filename.split('.')[-1]
            hashed_filename = ('%s%s%s'%(current_user.get_id(), current_time, form.postImage.data.filename))
            m.update(hashed_filename.encode('utf-8'))
            hashed_filename = ('%s.%s'%(m.hexdigest(), file_type))
            filename = upload.save(form.postImage.data, name=hashed_filename)
            print(filename)
            print(upload.url(filename))

        post = Post(accountID=current_user.get_id(), postContent=form.postContent.data, postTime=datetime.utcnow(), postImage=hashed_filename)
        db.session.add(post)
        db.session.commit()

    return render_template('post.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(email=form.email.data).first()
        if account is None or not account.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(account, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    else:
        print(form.errors)
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        account = Account(username=form.username.data, email=form.email.data, displayName=form.display_name.data)
        account.set_password(form.password.data)
        db.session.add(account)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/user/<username>')
def user(username):
    user = Account.query.filter_by(username=username).first_or_404()
    print(user.profileInfo)
    return 'ok'

@bp.route('/editProfile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    user = Account.query.get(current_user.get_id())
    username = user.username
    
    if form.validate_on_submit():
        username = form.username.data
        profileInfo = form.profileInfo.data
        Account.query.filter_by(accountID=current_user.get_id()).update({'username':username, 'profileInfo':profileInfo})
        db.session.commit()
        return 'changed'
    
    return render_template('edit.html', username=username, form=form)
    

@bp.route('/setting')
def setting():
    category = Category(categoryName='Gossip')
    db.session.add(category)
    db.session.commit()


