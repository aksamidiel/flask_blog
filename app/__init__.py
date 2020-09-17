from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import logging  # для вывода лога ошибок
from logging.handlers import SMTPHandler  #
from logging.handlers import RotatingFileHandler
import os

from flask_mail import Mail
from flask_bootstrap import Bootstrap  # для внешнего оформления
from flask_moment import Moment  # применяется для решения проблем с датами
from flask_babel import Babel  # для переводов
from flask_babel import lazy_gettext as _l
from flask import request

db = SQLAlchemy()  # add database SQLALCHEMY
migrate = Migrate()  # add mechanism migrations
login = LoginManager()  # add auth logic
login.login_view = 'auth.login'  # add secure about login user's
login.login_message = _l("Please LogIn to access this page")

mail = Mail()  # экземпляр класса mail
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # применение параметров из конфигурационного файла

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:  # для отправки ошибок на почту
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog failure',
                credentials=auth, secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

            if not os.path.exists('logs'):  # для записи логов
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: '
                                                        '%(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Microblog startup')

    return app


from app.errors import bp as errors_bp

current_app.register_blueprint(errors_bp)


# позволяет выбирать язык для перевода
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
