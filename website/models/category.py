from .base_model import BaseModel
from .. import db

class Category(BaseModel):
    """Categories table"""
    __tablename__ = 'categories'
    category_name = db.Column(db.String(128))
    events = db.relationship('Event', backref='category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

 