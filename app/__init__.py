from flask import Flask
from flask.ext.moment import Moment
from flask.ext.mail import Mail
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from werkzeug import secure_filename



app = Flask(__name__)
mail = Mail()
bootstrap = Bootstrap()
login_manager = LoginManager()
moment = Moment()
db = SQLAlchemy()
# config
app.config.from_object('config')
# social auth

# login manager
login_manager.init_app(app)
# show the login manager where the view is locate else the @login_required won't locate it
login_manager.login_view = 'auth.login'
# keep track of clients IP address and browser, logout if they change
login_manager.session_protection ='strong'




def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    
#register a blueprint

    from app.auth import auth as auth
    app.register_blueprint(auth)

    from app.main import main as main
    app.register_blueprint(main)
    
    return app
