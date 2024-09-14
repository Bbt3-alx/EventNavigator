from flask import Blueprint, render_template, redirect, url_for, request, flash
import re
from .models.user import User
from .models.event import Event
from .models.category import Category
from .models.registration import Registration
from .models.location import Location
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    """Login for existing user"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Loged in succefully !", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password !", category='error')
        else:
            flash("Email does not exist.", category='error')
    
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """Logout the current user"""
    logout_user()
    return redirect(url_for('auth.login'))

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
        password_match = '^[a-zA-Z0-9\W*]'

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
        elif not re.match(password_match, password1):
            flash('Password must be at least 8 character with \nCapitalcase and lowercase and number and character!', category='error')
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
            flash("Account created !", category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Manage user profile"""
    user = current_user
    print(user.user_name)

    if not user:
        flash('This user don\'t exist !', category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Update user info
        user.user_name = user_name
        user.email = email
        
        # Check if the old password matches the user's password
        if not check_password_hash(user.password, old_password):
            flash('Incorrect old password, please try again.', category='error')
            return redirect(url_for('auth.profile'))
        elif old_password == new_password:
            flash('New password cannot be the same as the old password!', category='error')
            return redirect(url_for('auth.profile'))
        elif new_password != confirm_password:
            flash('New password and confirmation do not match!', category='error')
            return redirect(url_for('auth.profile'))
        else:
            # Update the password if everything is correct
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

        try:
            db.session.commit()
            flash('Profile updated successfully!', category='success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            db.session.rollback() # Rollback in case of any error
            flash('An error occurred while updating your profile. Please try again.', category='error')
            return redirect(url_for('auth.profile'))

    # Load user and their events
    my_events = Event.query.filter_by(created_by=user.id).all()
    
    return render_template('profile.html', user=user, my_events=my_events)
            

            

