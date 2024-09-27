
from .base_model import BaseModel
from .. import db

class User(BaseModel):
    """The user table"""
    __tablename__ = 'users'
    auth0_id = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    picture = db.Column(db.String(1024))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    registrations = db.relationship('Registration')
    events = db.relationship('Event', backref='creator')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
