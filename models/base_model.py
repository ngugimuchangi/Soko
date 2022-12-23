#!/usr/bin/python3
""" Base class module
        Definition of Base class, it attributes,
        and methods
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()


class BaseModel:
    """ Base Model
        Public instance attributes:
            id (str): universally unique identifier (UUID) of the object
            created_at (datetime): when the object was created
            update_at (datetime): when the object was last updated

        Public instance methods:
            __init__: instantiation method
            __str__: string representation method
            save: update method
            to_dict: dictionary conversion method
            delete: deletes object from database storage
    """

    # Common fields across tables
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a new model"""
        self.id = uuid4().hex
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self.__class__, key) and \
                   key not in ["id", "created_at",
                               "updated_at"]:
                    setattr(self, key, value)

    def __str__(self):
        """ String representation method
            Args: none
            Return: string representation of the
                    BaseModel instance
        """
        cls = self.__class__.__name__
        obj_dict = self.__dict__.copy()
        if '_sa_instance_state' in obj_dict.keys():
            del obj_dict['_sa_instance_state']
        return "[{}] ({}) {}".format(cls, self.id, obj_dict)

    def save(self):
        """ Method to update updated_at attribute
            Args: none
            Return: nothing
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """ Dictionary representation method
            Args: none
            Return: dictionary representation of
                    instance
        """
        my_dict = self.__dict__.copy()
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()

        # Card expiring date
        if my_dict.get("expiry_date"):
            my_dict.update({"expiry_date": my_dict.get(
                           "expiry_date").isoformat()})

        # remove password and salt from dictionary
        # representation if they exist
        if my_dict.get("password"):
            my_dict.pop("password")
        if my_dict.get("salt"):
            my_dict.pop("salt")

        # delete _sa_instance_state from dictionary
        my_dict.pop("_sa_instance_state")
        return my_dict

    def delete(self):
        """Delete current instance from storage
           Args: None
           Return: nothing
        """
        from models import storage
        storage.delete(self)
