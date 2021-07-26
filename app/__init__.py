from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from .config import config
from logging.config import fileConfig
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.cfg.stdout')
fileConfig(log_file_path)

db = SQLAlchemy()
mail = Mail()

LOAD_DUMMY_DATA = True

def create_app(config_name='development'):
    app = Flask(__name__)
    config[config_name].init_app(app)
    app.config.from_object(config[config_name])

    CORS(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import (
        User,
        ReportingEntity,
        EntityProperty,
        EntityToSubentity,
        UserToEntity,
        SuperUser,
    )

    db.create_all(app=app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .profile import profile as profile_blueprint
    from .map import map as map_blueprint
    from .superuser_dash import superuser_dashboard as super_dash_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(map_blueprint)
    app.register_blueprint(super_dash_blueprint)

    return app
