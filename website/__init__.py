from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_migrate import Migrate


load_dotenv()  # Load environment variables from a .env file

db = SQLAlchemy() 


# Fetch environment variables
EVENT_NAVIGATOR_USER = getenv('EVENT_NAVIGATOR_USER')
EVENT_NAVIGATOR_PWD = getenv('EVENT_NAVIGATOR_PWD')
EVENT_NAVIGATOR_HOST = getenv('EVENT_NAVIGATOR_HOST')
EVENT_NAVIGATOR_DB = getenv('EVENT_NAVIGATOR_DB')
EVENT_NAVIGATOR_ENV = getenv('EVENT_NAVIGATOR_ENV')

print(EVENT_NAVIGATOR_USER, EVENT_NAVIGATOR_PWD, EVENT_NAVIGATOR_HOST, EVENT_NAVIGATOR_DB)

def create_app():
    app = Flask(__name__)


    # Set up the configuration
    app.config['SECRET_KEY'] = 'MY KEY SECRET'
    app.config['UPLOAD_FOLDER'] = getenv('UPLOAD_FOLDER')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(EVENT_NAVIGATOR_USER,
                    EVENT_NAVIGATOR_PWD,
                    EVENT_NAVIGATOR_HOST,
                    EVENT_NAVIGATOR_DB
                    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Initialize the database with the app
    db.init_app(app)

    migrate = Migrate(app, db)

    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models
    from .models import User

    # Ensure the tables are created
    with app.app_context():
        db.create_all()


    # Setup LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # Load a user
        return User.query.get(id)

    return app


