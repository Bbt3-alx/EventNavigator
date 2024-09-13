from flask import Blueprint, render_template, redirect, url_for, request, flash
import re
from .models import User
from .models import Event
from .models import Category
from .models import Registration
from .models import Location
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

auth.route('/profile/<id>', methods=['GET', 'POST'])
login_required
def profile(id):
    """Manage user profile"""
    user = User.query.filter_by(id=id).first()

    if user:
        if request.method == 'POST':
            user_name = request.form.get('user_name')
            email = request.form.get('email')
            old_password = request.form.get('old_pasword')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_pasword')

            user.user_name = user_name
            user.email = email
            if check_password_hash(old_password) != check_password_hash(user.password):
                flash('Incorect password, please enter your old password.', category='error')
            elif check_password_hash(old_password) == generate_password_hash(new_password):
                flash('There is no difference between the old and the new password !', category='error')
            elif new_password != confirm_password:
                flash('Password are not same, please try again!', category='error')
            else:
                user.password = new_password
            
            db.session.add(user)

            try:
                db.session.commit()
                flash('Profile updated !', category='success')
                return redirect(url_for('profile'))
            except Exception as e:
                flash('An exception occured.', category='error')
                return redirect(url_for('profile'))
        else:
            user = User.query.all()
            my_events = Event.query.filter_by(created_by=id).all()
    flash('This user don\'t exist !', category='error')

    return render_template('profile.html', user=user, my_events=my_events)
            

            

