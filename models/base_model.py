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
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key not in ['__class__', 'created_at', 'updated_at']:
                    setattr(key, value, self)

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
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()

        # delete _sa_instance_state from dictionary
        if '_sa_instance_state' in my_dict.keys():
            del my_dict['_sa_instance_state']
        return my_dict

    def delete(self):
        """Delete current instance from storage
           Args: None
           Return: nothing
        """
        from models import storage
        storage.delete(self)
