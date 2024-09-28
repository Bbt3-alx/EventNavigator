import os
from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from .models.event import Event
from .models.category import Category
from .models.user import User
from . import db
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from sqlalchemy.orm import joinedload


views = Blueprint('views', __name__, static_folder="static", template_folder="templates")


@views.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.args.get('search_query', '')
    selected_category = request.args.get('category', '') 

    # Start with all events
    events = Event.query

    # If there's a search query, filter events by title or description
    if search_query:
        events = events.filter(
            or_(
                Event.title.ilike(f'%{search_query}%'), 
                Event.description.ilike(f'%{search_query}%'),
                Event.date.ilike(f'%{search_query}%')
            )
        )
    
    # If a category is selected, filter by category
    if selected_category:
        events = events.filter_by(category_id=selected_category)
    
    # Execute query to get filtered events
    events = events.options(joinedload(Event.creator)).all()

    # Fetch all categories to populate the dropdown
    categories = Category.query.all()

    #author = User.query.filter_by(id=Event.created_by).first()

    return render_template("home.html", user=current_user, events=events, categories=categories)


@views.route('/about', methods=['GET', 'POST'])
def about():
    """About me"""
    return render_template('about.html', user=current_user)


@views.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    """Allows authenticated users to create a new event"""
    categories = Category.query.all()  # Fetch all categories

    if request.method == 'POST':
        new_event = None  # Initialize new_event to None
        event_image = None # Initialize event_image to None
        

        # Handle the POST request (create a new event)
        selected_category_id = request.form.get('category')
        event_title = request.form.get('event_title')
        event_date = request.form.get('event_date')
        description = request.form.get('description')
        location = request.form.get('location')

        category = db.session.query(Category).get(selected_category_id)
       
        if not category:
            flash('Invalid category selected', 'error')
            return redirect(url_for('views.create_event'))
        
        image_source = request.form.get('imageSource')
        if image_source == 'upload':
            image = request.files.get('file')
            if image:
                event_image = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], event_image)
                if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                    os.makedirs(current_app.config['UPLOAD_FOLDER'])
                image.save(image_path) # Store the image path in the database

        elif image_source == 'link':
            event_image = request.form.get('imageLinkInput')
            if not event_image:
                flash('Invalid image link. Please provide a valid URL.', 'error')

        new_event = Event(
            title=event_title,
            date=event_date,
            description=description,
            event_image=event_image,
            location = location,
            created_by=current_user.id,
            category_id=category.id
        )


        if new_event:
            db.session.add(new_event)
            try:
                db.session.commit()
                flash(f'{new_event.title} created successfully !', 'success')
                return redirect(url_for('views.home'))
            except Exception as e:
                db.session.rollback()
                flash(f'An unknown error occurred', 'error')
                return redirect(url_for('views.create_event'))
        else:
            flash('Event creation failed. Please provide a valid image or link.', 'error')
            return redirect(url_for('views.create_event'))
        
    return render_template("create_event.html", categories=categories, user=current_user)


@views.route('/update_event/<id>', methods=['GET', 'POST'])
@login_required
def update_event(id):
    """Update an event"""
    event = Event.query.filter_by(id=id).first()
    
    if request.method == 'POST':

        if not event:
            flash('Event not found', category='error')
            return redirect(url_for('views.home'))
        
        # Handle the POST request (update an existing event)
        title = request.form.get('event_title')
        date = request.form.get('event_date')
        description = request.form.get('description')
        image_source = request.form.get('imageSource')

        if image_source == 'upload':
            image = request.files.get('file')
            if image:
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                    os.makedirs(current_app.config['UPLOAD_FOLDER'])
                image.save(image_path) # Store the image path in the database

                event.event_image = filename

        elif image_source == 'link':
            image_link = request.form.get('imageLinkInput')
            if image_link:
                event.event_image = image_link
            else:
                flash('Invalid image link. Please provide a valid URL.', 'error')
        
        if event:
            event.title = title
            event.description = description
            event.date = date
            try:
                db.session.commit()
                flash(f'{event.title} Updated successfully!', 'success')
                return redirect(url_for('views.home'))
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('views.update_event'))
        else:
            flash('Event update failed. Please provide a valid image or link.', 'error')
            return redirect(url_for('views.update_event'))
    return render_template('event_update.html', user=current_user, event=event)


@views.route('/delete_event/<id>', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    """Delete an event by its id"""
    event = Event.query.filter_by(id=id).first()

    if event:
        try:
            db.session.delete(event)
            flash(f"Event {event.title} deleted succefully !", category='success')
            db.session.commit()
            return redirect(url_for('auth.profile'))
        except Exception as e:
            flash(f'An error occured when deleting {event.title}.', category='error')
            return redirect(url_for('auth.profile'))
    return render_template('profile.html', event=event)

        

@views.route('/event/<id>', methods=['GET', 'POST'])
def event(id):
    """Get a specific event by its id"""
    event = Event.query.filter_by(id=id).first()
    category = Category.query.filter_by(id=event.category_id).first()
    author = User.query.filter_by(id=event.created_by).first()
    created_by = author.user_name

    if event:
        return render_template('event_details.html', created_by=created_by, user=current_user, event=event, category=category)
    return redirect(url_for('views.home'))


@views.route('/manage_categories', methods=['GET', 'POST'])
def manage_categories():
    """Allows admin to add and manage categories"""
    
    # Fetch all categories
    categories = Category.query.all()
    if current_user.is_authenticated:
            if request.method == 'POST':
                category_name = request.form.get('category_name')

                # Check if category already exist
                category_exit = Category.query.filter_by(category_name=category_name).first()
                if category_exit:
                    flash('Category already exists.', 'error')
                else:
                    # Add new category
                    new_category = Category(category_name=category_name)
                    db.session.add(new_category)
                    db.session.commit()
                    flash(f'Category "{new_category.category_name}" created successfully!', 'success')
                    redirect(url_for('views.manage_categories'))

            return render_template('manage_categories.html', user=current_user, categories=categories)
    else:
        return render_template('manage_categories.html', user=current_user, categories=categories)


@views.route('/events_by_category/<id>', methods=['GET', 'POST'])
def events_by_category(id):
    """Retrieve all the event of a category"""
    categories = Category.query.all()
    events_by_category = Event.query.options(joinedload(Event.creator)).filter_by(category_id=id).all()
    

    return render_template(
        'events.html',
        user=current_user,
        categories=categories,
        events_by_category=events_by_category
    )
