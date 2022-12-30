#!/usr/bin/python3
""" Customer class module
        Definition of Buyer class, it attributes,
        and methods
"""
from flask_login import UserMixin
from hashlib import sha256
from models.base_model import Base, BaseModel
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from uuid import uuid4


class Customer(BaseModel, Base, UserMixin):
    """ Customer class representing customer table
        Attributes:
            first_name (str): customer's first name
            last_name (str): customer's last name
            region_code (str): customer's region code
            phone_number (str): customer's phone number
            email (str): customer's email address
            password (str): customer's hashed password
            salt (str): salt used to hash password
            confirmed(str): confirmation status
            card: relationship with cards table
            cart: relationship with cart table
            notifications: relationship with customer_notifications table
            saved_items: relationship with saved_items table
            shipping_addresses: relationship with shipping address
                              table
    """
    __tablename__ = "customers"

    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    phone_number = Column(String(60), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    salt = Column(String(60), nullable=False)
    confirmed = Column(Boolean, default=False, nullable=False)
    cards = relationship('CustomerCard',
                         backref="customer",
                         cascade="all,delete")
    cart = relationship("Cart",
                        backref="customer",
                        cascade="all,delete")
    notifications = relationship("CustomerNotification",
                                 backref="customer",
                                 cascade="all,delete")
    saved_items = relationship("SavedItem",
                               backref="customer",
                               cascade="all,delete")
    addresses = relationship("ShippingAddress",
                             backref="customer",
                             cascade="all,delete")

    def __init__(self, **kwargs):
        """Instantiates the Customer object."""
        # Add salt and hash password
        salt = uuid4().hex
        password = kwargs.get("password")
        password = sha256("{}{}".format(password, salt).
                          encode('utf-8')).hexdigest()
        kwargs.update({"password": password, "salt": salt})

        super().__init__(**kwargs)
