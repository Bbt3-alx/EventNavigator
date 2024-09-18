import uuid
from flask_login import UserMixin
from datetime import datetime
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from .. import db

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


    def to_dict(self, exclude_sensitive=True):
        """Returns a dictionary containing all keys/values of the instance.
        Optionally excludes sensitive fields like password.
        """
        # Copy the instance's __dict__ to avoid modifying the original
        new_dict = self.__dict__.copy()

        # Format date fields (assuming 'created_at' and 'updated_at' are datetime objects)
        if "created_at" in new_dict and isinstance(new_dict["created_at"], datetime):
            new_dict["created_at"] = new_dict["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        if "updated_at" in new_dict and isinstance(new_dict["updated_at"], datetime):
            new_dict["updated_at"] = new_dict["updated_at"].strftime("%Y-%m-%d %H:%M:%S")

        # Add class name to the dictionary
        new_dict["__class__"] = self.__class__.__name__

        # Remove SQLAlchemy internal state if present
        new_dict.pop("_sa_instance_state", None)

        # Exclude sensitive fields like password
        if exclude_sensitive and "password" in new_dict:
            del new_dict["password"]

        return new_dict

