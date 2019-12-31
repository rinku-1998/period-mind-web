from app import db, api_login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Account(UserMixin, db.Model):
    accountID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), index=True, unique=True)
    displayName = db.Column(db.String(30), index=True)
    profileInfo = db.Column(db.String(100))
    avatar = db.Column(db.String(100), unique=True)
    createTime = db.Column(db.DateTime)
    relation_postedAccount = db.relationship('Post', backref='account', lazy='select')
    relation_commentAccount = db.relationship('Comment', backref='account', lazy='select')
    relation_friendInAccount = db.relationship('Friend', backref='account', lazy='select')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def id(self):
        return self.accountID

@api_login.user_loader
def load_account(id):
    return Account.query.get(int(id))


class Category(db.Model):
    categoryID = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(20), index=True, unique=True)
    relation_postedCategory = db.relationship('Post', backref='category', lazy='select')

class Post(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, db.ForeignKey('account.accountID'))
    categoryID = db.Column(db.Integer, db.ForeignKey('category.categoryID'))
    postContent = db.Column(db.String(150))
    postImage = db.Column(db.String(100))
    postLikeNumber = db.Column(db.Integer, default=0)
    postLikeAccount = db.Column(db.Integer)
    postCheck = db.Column(db.Boolean)
    postLocation = db.Column(db.String(30))
    postTime = db.Column(db.DateTime)
    relation_commentInPost = db.relationship('Comment', backref='post', lazy='select')

class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    postID = db.Column(db.Integer, db.ForeignKey('post.postID'))
    accountID = db.Column(db.Integer, db.ForeignKey('account.accountID'))
    commentContent = db.Column(db.String(100))
    commentImage = db.Column(db.String(100))
    commentTime = db.Column(db.DateTime)

class Friend(db.Model):
    friendID = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, db.ForeignKey('account.accountID'))
    friendAccountID = db.Column(db.Integer, nullable=False)
