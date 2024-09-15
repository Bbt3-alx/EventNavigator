from . import api_views, generate_api_key, generate_secret
from website.models.user import User
from website.models.api_client import ApiClient
from website import db
from flask import abort, jsonify, make_response, request
from flask_login import current_user, login_required


@api_views.route('/login', methods=['POST'])
def login():
    """Authenticates external clients using their API key."""
    api_key = request.form.get('api_key')
    secret = request.form.get('secret_key')

    api_keys = ApiClient.query.filter_by(api_key=api_key).first()
    if not api_keys:
        print(f"API_KEY:{api_key}")
        print(f"SECRT: {secret}")
        return make_response(jsonify({'error': 'Invalide API KEY, SECRET or inactive account.'}), 403)
    
    # Return a session token for future authentication
    return make_response(jsonify({
        'message': 'Authentication successful',
        'session_token': f'default_session_token {secret}'
    }), 200)


@api_views.route('/register', methods=['POST'])
def register():
    """Allows external clients to register for API access."""
    email = request.form.get('email')

    if not email:
        return jsonify({'error': 'Missing required fields'}), 400
    
    email_exist = ApiClient.query.filter_by(email=email).first()

    if email_exist:
        return make_response(jsonify({'error': 'This email already exist'}), 409)

    api_key = generate_api_key()
    secret = generate_secret()
    
    new_key = ApiClient(
        api_key=api_key,
        secret_key=secret,
        email=email
    )

    db.session.add(new_key)
    db.session.commit()
    

    return make_response(jsonify({
            'message': 'Registration Successful',
            'api_key': api_key,
            'secret': secret
            }), 201)
