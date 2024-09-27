"""Bluprint for API"""
from flask import Blueprint
from website.models.api_client import ApiClient


api_views = Blueprint('api_views', __name__, url_prefix='/api/v1')


from functools import wraps
import secrets


# Generate API key
def generate_api_key():
    return secrets.token_urlsafe(32) # Generates a 32-character API key


# Generate API secret
def generate_secret():
    return secrets.token_urlsafe(64) # Generates a 64-character API secret


# API key authentication decorator
def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.form.get('api_key')
        secret = request.form.get('secret_key')

        api_records = ApiClient.query.filter_by(api_key=api_key, secret_key=secret).first()

        if api_records:
            if not api_records or not api_records.is_active():
                return jsonify({'Error': 'Invalide api key, secret or inactive key'}), 403
            return f(*args, **kwargs)
    return decorated_function


'''
def validate_api_key(api_key, secret):
    client = db.session.query(ApiClient).filter_by(api_key=api_key).first()
    if not client or not check_password_hash(client.scret_key, secret):
        return False
    return True
'''


from .api_user import *
from .api_event import *
from .api_categories import *
#from .api_location import *
from .api_login import *
