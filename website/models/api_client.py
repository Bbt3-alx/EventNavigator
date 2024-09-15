from .base_model import BaseModel
from .. import db
from datetime import datetime, timedelta

class ApiClient(BaseModel):
    __tablename__ = "api_client"
    api_key = db.Column(db.String(250), nullable=False)
    secret_key = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    expiration_date = db.Column(db.Date, default=lambda:datetime.now() + timedelta(days=5))
    email = db.Column(db.String(250), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def activate(self):
        """Mark API key as active."""
        self.is_active = True
        db.session.commit()

    def deactivate(self):
        """Mark API key as inactive."""
        self.is_active = False
        db.session.commit()

    def is_active(self):
        """Check if the API key is active or not"""
        return self.is_active