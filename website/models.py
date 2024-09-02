"""This module contain all the model for event navigator"""
from . import db
from flask_login import UserMixin
from datetime import datetime
import uuid
from sqlalchemy import ForeignKey


time = "%Y-%m-%d-%H:%M:%S.%f"


class BaseModel(db.Model, UserMixin):
    """The Base model"""
    __abstract__ = True
    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.now()
            if kwargs.get("updated_at", None) and type(self.created_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.now()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()


class User(BaseModel):
    """The user table"""
    __tablename__ = 'users'
    user_name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    user_image = db.Column(db.String(256))
    registrations = db.relationship('Registration')
    events = db.relationship('Event', backref='creator')
    
    
class Category(BaseModel):
    """Categories table"""
    __tablename__ = 'categories'
    category_name = db.Column(db.String(128))
    events = db.relationship('Event', backref='category')

    
class Event(BaseModel):
    """Event table"""
    __tablename__ = 'events'
    title = db.Column(db.String(250))
    description = db.Column(db.String(1024))
    date = db.Column(db.DateTime, default = datetime.now())
    event_image = db.Column(db.String(256))
    created_by = db.Column(db.String(60), db.ForeignKey('users.id'))
    category_id = db.Column(db.String(60), db.ForeignKey('categories.id'))
    locations_id = db.Column(db.String(60), db.ForeignKey('locations.id'))
    registrations = db.relationship('Registration', backref='event')


class Location(BaseModel):
    """The location table"""
    __tablename__ = 'locations'
    location_name = db.Column(db.String(128))
    adrress = db.Column(db.String(128))
    city = db.Column(db.String(128))
    state = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    events = db.relationship('Event', backref='location')


class Registration(BaseModel):
    """Table registration"""
    __tablename__ = 'registrations'
    registrered_at = db.Column(db.DateTime, default = datetime.now())
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    event_id = db.Column(db.String(60), db.ForeignKey('events.id'))
