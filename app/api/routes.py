from app import db, api_login, upload
from app.api.forms import LoginForm, PostForm, RegisterForm, EditProfileForm, CommentForm
from app.api.models import Account, Post, Category, Comment

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.api import bp

from datetime import datetime
from app.api.sql2ary import sql2ary, comment_sql2ary
import hashlib


@bp.route('/index')
@login_required
def index():
    # Load with SQL syntax
    syntax = 'SELECT account.username, post.* FROM post JOIN account ON account.accountID == post.accountID ORDER BY post.postTime desc'
    result = db.session.execute(syntax)
    posts = sql2ary(result)
    # print(result)
    # Load with DB-ORM
    # posts = Post.query.join(Account).filter(Account.accountID == Post.accountID).all()
    # posts = Post.query.join(Account, (Account.accountID == Post.accountID)).all()
    # names = [row[0] for row in result]
    # print (names)
    
    # for post in posts:
    #     print(vars(post))
    # return render_template('index.html', posts=posts)
    return jsonify(posts)
    
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

@bp.route('/comment', methods=['GET', 'POST'])
@login_required
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        hashed_filename = None #Default for no file uploaded
        if not form.commentImage.data.filename == '':
            m = hashlib.md5()
            current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            file_type = form.commentImage.data.filename.split('.')[-1]
            hashed_filename = ('%s%s%s'%(current_user.get_id(), current_time, form.commentImage.data.filename))
            m.update(hashed_filename.encode('utf-8'))
            hashed_filename = ('%s.%s'%(m.hexdigest(), file_type))
            filename = upload.save(form.commentImage.data, name=hashed_filename)
            print(filename)
            print(upload.url(filename))

        comment = Comment(postID=form.postID.data, accountID=current_user.get_id(), commentContent=form.commentContent.data, commentTime=datetime.utcnow(), commentImage=hashed_filename)
        db.session.add(comment)
        db.session.commit()

    return render_template('comment.html', form=form)

@bp.route('/getComment/<postID>', methods=['GET'])
@login_required
def getComment(postID):
    syntax = ('SELECT account.username, comment.* FROM comment JOIN account ON account.accountID == comment.accountID and comment.postID = %s ORDER BY comment.commentTime asc'%postID)
    result = db.session.execute(syntax)
    # print(result)
    comments = comment_sql2ary(result)

    return jsonify(comments)



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('api.index'))
    form = LoginForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(email=form.email.data).first()
        if account is None or not account.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('api.login'))
        login_user(account, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('api.index')
        # return redirect(next_page)
        return 'ok'
    else:
        print(form.errors)
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('api.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('api.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        account = Account(username=form.username.data, email=form.email.data, displayName=form.display_name.data, createTime=datetime.utcnow())
        account.set_password(form.password.data)
        db.session.add(account)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('api.login'))
    return render_template('register.html', form=form)

@bp.route('/myprofile')
@login_required
def myprofile():
    user = Account.query.filter_by(accountID=current_user.get_id()).first_or_404()
    user_list = {}
    if user:
        user_list['username'] = user.username
        user_list['display_name'] = user.displayName
        user_list['email'] = user.email
        user_list['profile_info'] = user.profileInfo
        user_list['avatar'] = user.avatar
        time = user.createTime
        time_string = datetime.strftime(time, '%Y-%m-%d')
        time_element = time_string.split('-')
        user_list['createTime'] = ('%s年%s月%s日 加入'%(time_element[0], time_element[1], time_element[2])) 

    return jsonify(user_list)

@bp.route('/user/<username>')
def user(username):
    user = Account.query.filter_by(username=username).first_or_404()
    user_list = {}
    if user:
        user_list['username'] = user.username
        user_list['display_name'] = user.displayName
        user_list['email'] = user.email
        user_list['profile_info'] = user.profileInfo
        user_list['avatar'] = user.avatar
        time = user.createTime
        time_string = datetime.strftime(time, '%Y-%m-%d')
        time_element = time_string.split('-')
        user_list['createTime'] = ('%s年%s月%s日 加入'%(time_element[0], time_element[1], time_element[2])) 

    return jsonify(user_list)

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


