from flask import Blueprint, session, jsonify, render_template, redirect, url_for, request, flash
import re
from .models.user import User
from .models.event import Event
from . import db, oauth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from authlib.integrations.flask_client import OAuth, OAuthError
from flask import current_app as app 


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    """Redirect to Auth0 for login"""
    return oauth.auth0.authorize_redirect(redirect_uri=url_for('auth.callback', _external=True))

@auth.route('/callback')
def callback():
    """ Handle the callback from Auth0 after login """
    if 'error' in request.args:
        error_description = request.args.get('error_description', 'Something went wrong during login.')
        flash(f'Login failed: {error_description}', category='error')
        return redirect(url_for('views.home'))
    
    try:
        token = oauth.auth0.authorize_access_token()
        session['user'] = token
        user_info = oauth.auth0.get('userinfo').json()

        picture_url = user_info['picture']

        # Process user information here (e.g., create user if not exists)
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(
                auth0_id=user_info['sub'],
                user_name=user_info['name'],
                email=user_info['email'],
                picture=picture_url
                )
            db.session.add(user)
        else:
            user.picture = picture_url
            
        db.session.commit()

        login_user(user)
        return redirect(url_for('views.home'))
    except OAuthError as e:
        flash(f'Authorization error: {e.description}', category='error')
        return redirect(url_for('views.home'))


@auth.route('/logout', methods=["GET", "POST"])
def logout():
    """ Log out of Auth0 and remove session """
    logout_user()
    session.clear()
    return redirect(
        f"https://{app.config['AUTH0_DOMAIN']}/v2/logout?client_id={app.config['AUTH0_CLIENT_ID']}&returnTo={url_for('views.home', _external=True)}"
    )

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    """Sign Up for new users"""
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        
        # Validate user data
        email_match = '^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$'

        # Check if email already exist
        user = User.query.filter_by(email=email).first()

        if user:
            flash(f'{email} already exists. ', category='info')
        elif len(email) < 5:
            flash("Your email is too short, try again !", category='error')
        elif not re.match(email_match, email):
            flash("Invalid email !", category='error')
        elif len(user_name) < 2:
            flash("First name must be greater than 2 !", category='error')
        elif len(password1) < 7:
            flash("Password should be at least 8 characters.", category='error')
        elif password1 != password2:
            flash("Password don't match.", category='error')
        else:
            # Add the new user
            new_user = User(
                user_name=user_name,
                email=email,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created ! ", category='info')
            login_user(new_user)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Manage user profile"""
    user = current_user

    if not user:
        flash('This user don\'t exist !', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        try:
            # Update user info
            user.user_name = user_name
            user.email = email

            # Check if the old password matches the user's password
            if not check_password_hash(user.password, old_password):
                flash('Incorrect old password, please try again.', category='error')
                return redirect(url_for('auth.profile'))
            
            # Check if new password and confirm password match
            elif new_password != confirm_password:
                flash('New password and confirmation do not match!', category='error')
                return redirect(url_for('auth.profile'))
            
            else:
                # Update the password if everything is correct
                user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                db.session.commit()
                flash('Profile updated successfully!', category='success')
                return redirect(url_for('auth.profile'))

        except db.exc.IntegrityError: 
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', category='error')
            return redirect(url_for('auth.profile'))

    return render_template('profile.html', user=user)
@auth.route('/my_events', methods=['GET', 'POST'])
@login_required
def my_events():
    """Loads user events"""
    # Load user and their events
    user = current_user
    my_events = Event.query.filter_by(created_by=user.id).all()

    return render_template('my_events.html', user=current_user, my_events=my_events)
            