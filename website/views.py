from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from .models import Event, db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """The home page"""
    if request.method == 'POST':
        event_title = request.form.get('event_title')
        event_date = request.form.get('event_date')
        description = request.form.get('description')
        image = request.form.get('description')

        new_event = Event(
            title=event_title,
            date=event_date,
            description=description,
            event_image=image,
            created_by=current_user.id
        )

        db.session.add(new_event)
        db.session.commit()
        flash(f'Event created with id {new_event.id} created by {current_user.user_name}')
    return render_template("home.html", user=current_user)