from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask_migrate import Migrate
import os


load_dotenv()  # Load environment variables from a .env file

db = SQLAlchemy()
oauth = OAuth()

def create_app(config_name="production"):
    """Create a Flask app instance with the specified configuration."""
    app = Flask(__name__)


    # Use the configuration from the config.py file
    if config_name is None:
        config_name = os.getenv('EVENT_NAVIGATOR_ENV', 'development')  # Default to 'development'
    
    app.config.from_object(f'config.{config_name.capitalize()}Config')  # Load the config class

    # Configure Auth0
    
    oauth.init_app(app)

    oauth.register(
        'auth0',
        client_id=app.config['AUTH0_CLIENT_ID'],
        client_secret=app.config['AUTH0_CLIENT_SECRET'],
        api_base_url=f"https://{app.config['AUTH0_DOMAIN']}",
        access_token_url=f"https://{app.config['AUTH0_DOMAIN']}/oauth/token",
        authorize_url=f"https://{app.config['AUTH0_DOMAIN']}/authorize",
        jwks_uri=f"https://{app.config['AUTH0_DOMAIN']}/.well-known/jwks.json",
        client_kwargs={
            'scope':'openid profile email',
        },
    )

    # Initialize the database with the app
    db.init_app(app)
    migrate = Migrate(app, db)


    # Setup LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Load a user
        return User.query.get(user_id)
    
    login_manager.init_app(app)


    from .views import views
    from .auth import auth
    from website.api.v1.views import api_views

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.register_blueprint(api_views)

    from .models.user import User

    # Ensure the tables are created
    with app.app_context():
        db.create_all()

    return app
