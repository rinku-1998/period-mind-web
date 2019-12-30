from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
migrate = Migrate()
main_login = LoginManager()
api_login = LoginManager()
# login.login_view = 'login'
upload = UploadSet(name='images', extensions=IMAGES)
# configure_uploads(app, upload)