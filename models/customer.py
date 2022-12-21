#!/usr/bin/python3
""" Customer class module
        Definition of Buyer class, it attributes,
        and methods
"""
from hashlib import sha256
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from uuid import uuid4


class Customer(Base, BaseModel):
    """ Customer class representing customer table
        Attributes:
            first_name (str): customer's first name
            last_name (str): customer's last name
            region_code (str): customer's region code
            phone_number (str): customer's phone number
            email (str): customer's email address
            password (str): customer's hashed password
            salt (str): salt used to has password
            card: relationship with cards table
            cart: relationship with cart table
            chats: relationship with chats table
            notifications: relationship with notifications table
            reviews: relationship with reviews table
                     shouldn't cascade on delete. Cascade set
                     to products table
            saved_items: relationship with saved_items table
            shipping_addresses: relationship with shipping address
                              table
    """
    __table__ = "customers"

    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    region_code = Column(String(60), nullable=False)
    phone_number = Column(String(60), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    salt = Column(String(60))
    card = relationship('CustomerCard', backref="customer", cascade="delete")
    cart = relationship("Cart", backref="customer", cascade="delete")
    chats = relationship("CustomerCard", backref="customer")
    notifications = relationship("CustomerNotification",
                                 backref="customer", cascade="delete")
    reviews = relationship("Cart", backref="customer")
    saved_items = relationship("SavedItems", backref="customer",
                               cascade="delete")
    shipping_addresses = relationship("Cart", backref="customer",
                                      cascade="delete")

    def __init__(self, **kwargs):
        """Initializes the Customer Object."""
        # Call parent init class to created shared attributes
        super().__init__()

        # Add salt and hash password
        salt = uuid4().hex
        password = kwargs.get('password')
        password = sha256("{}{}".format(password, salt).
                          encode('utf-8')).hexdigest()

        # Add other attributes
        kwargs.update({"password": password, "salt": salt})
        for key, value in kwargs:
            if key not in ["id", "created_at", "updated_at"]:
                setattr(self, key, value)
