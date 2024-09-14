from .base_model import BaseModel
from .. import db
from datetime import datetime

class Registration(BaseModel):
    """Table registration"""
    __tablename__ = 'registrations'
    registrered_at = db.Column(db.DateTime, default = datetime.now())
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    event_id = db.Column(db.String(60), db.ForeignKey('events.id'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)