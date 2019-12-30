from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.api.models import Account

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField('登入')

class RegisterForm(FlaskForm):
    username = StringField('名字', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    password2 = PasswordField('請再輸入一次密碼', validators=[DataRequired(), EqualTo('password')])
    display_name = StringField('顯示名稱', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('註冊')

    def validate_username(self, username):
        account = Account.query.filter_by(username=username.data).first()
        if account is not None:
            raise ValidationError('Please use a different username')
    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()
        if account is not None:
            raise ValidationError('Please use a different email')

class PostForm(FlaskForm):
    postContent = StringField('貼文內容', validators=[DataRequired()])
    postImage = FileField('選擇檔案')
    submit = SubmitField('發布')

class EditProfileForm(FlaskForm):
    username = StringField('名字', validators=[DataRequired()])
    display_name = StringField('顯示名稱', validators=[DataRequired()])
    profileInfo = StringField('個人簡介', validators=[DataRequired()])
    submit = SubmitField('確定更改')