from .base_model import BaseModel
from .. import db


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
