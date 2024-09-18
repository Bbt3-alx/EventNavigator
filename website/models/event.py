from .base_model import BaseModel
from .. import db
from datetime import datetime


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)