from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

# Initialize extensions
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    # Use the config dictionary to load the configuration
    app.config.from_object(config[config_name])
    # Initialize the app with the selected config class
    config[config_name].init_app(app)
    
    # Initialize exteions with the app
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    
    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app