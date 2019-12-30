from flask import Flask
from config import Config

from app.extensions import db, migrate, login, upload, configure_uploads

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # db = SQLAlchemy(app)
    # migrate = Migrate(app, db)
    # login = LoginManager(app)
    # login.login_view = 'login'
    # upload = UploadSet(name='images', extensions=IMAGES)
    # configure_uploads(app, upload)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'api.login'
    configure_uploads(app, upload)
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # from app import routes, models

    return app