
from .base_model import BaseModel
from .. import db

class User(BaseModel):
    """The user table"""
    __tablename__ = 'users'
    user_name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    user_image = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    registrations = db.relationship('Registration')
    events = db.relationship('Event', backref='creator')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def is_active(self):
        # Define your logic to check if the user is active
        return True  
