from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)


    app.config["SECRET_KEY"] = "9OLWxND4o83j4K4iuopO"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SECURITY_PASSWORD_SALT"] = "my_precious_two"
    app.config["DEBUG"] = False
    app.config["BCRYPT_LOG_ROUNDS"] = 13
    app.config["WTF_CSRF_ENABLED"] = True
    app.config["DEBUG_TB_ENABLED"] = False
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = "jeevan.bhoot@gmail.com"
    app.config['MAIL_PASSWORD'] = "kudahuogculkdjdu"
    app.config['MAIL_DEFAULT_SENDER'] = "jeevan.bhoot@gmail.com"

    db.init_app(app)
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app