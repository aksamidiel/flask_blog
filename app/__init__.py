from flask import Flask
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

app = Flask(__name__)
app.config.from_object(Config)  # применение параметров из конфигурационного файла
db = SQLAlchemy(app)  # add database SQLALCHEMY
migrate = Migrate(app, db)  # add mechanism migrations
login = LoginManager(app)  # add auth logic
login.login_view = 'login'  # add secure about login user's
login.login_message = _l("Please LogIn to access this page")

mail = Mail(app)  # экземпляр класса mail
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)

if not app.debug:
    if app.config['MAIL_SERVER']:  # для отправки ошибок на почту
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
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


# позволяет выбирать язык для перевода
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


from app import routes, models, errors

