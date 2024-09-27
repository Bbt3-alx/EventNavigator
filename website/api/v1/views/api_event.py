"""EVENTS ENDPOINT"""

from . import api_views, api_key_required
from website.models.event import Event
#from website.models.location import Location
from website import db
from .errors import not_found
from flask import jsonify, make_response, request
from werkzeug.utils import secure_filename
import os
from flask import current_app
from flask_login import current_user, login_required


@api_views.route('/events', methods=['GET'])
def get_events():
    """Retrieve a list of events, with optional filters for location and date."""
    location_query = request.args.get('location')
    date_query = request.args.get('date')
    

    # Filter by date and location if provided
    query = Event.query

    if location_query:
        location = query.filter_by(location=location_query).first()
        query = query.filter_by(location_id=location.id)
    
    if date_query:
        query = query.filter_by(date=date_query)
    
    events = query.all()

    all_events = []

    for event in events:
        all_events.append(event.to_dict())

    return make_response(jsonify(all_events), 200)


@api_views.route('/event/<event_id>', methods=['GET'])
def get_event(event_id):
    """Retrieve detailed information about a specific event."""
    event = Event.query.get_or_404(event_id)

    if event:
        return make_response(jsonify(event.to_dict()), 200)
    return not_found(404)


@api_views.route('/events', methods=['POST'])
@api_key_required
def create_event():
    """Allow external authenticated clients to create new events."""
    title = request.form.get('title')
    description = request.form.get('description')
    date = request.form.get('date')
    event_image = request.files.get('file')

    if event_image:
        filename = secure_filename(event_image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])
        event_image.save(image_path)

    if not all([title, description, date]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # create new event
    new_event = Event(
        title=title,
        description=description,
        date=date,
        event_image=event_image,
    )

    db.session.add(new_event)
    db.session.commit()

    return make_response(jsonify({'message': 'Event created successfully!', 'event_id': new_event.id}), 201)

