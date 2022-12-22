#!/usr/bin/python3
""" Seller class module
        Definition of Seller class, it attributes,
        and methods
"""
from hashlib import sha256
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from uuid import uuid4


class Seller(BaseModel, Base):
    """ Seller class representing sellers table
        Attributes:
            first_name (str): sellers's first name
            last_name (str): sellers's last name
            region_code (str): seller's region code
            phone_number (str): seller's phone number
            email (str): seller's email address
            password (str): customer's hashed password
            salt (str): salt used to hash password
            shop_status(int): shop status
            products: relationship with products table
            card: relationship with seller_cards table
            notifications: relationship with seller_notifications table
    """
    __tablename__ = "sellers"

    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    salt = Column(String(60))
    shop_status = Column(Integer, default=1, nullable=False)
    products = relationship("Product", backref="seller",
                            cascade="all,delete")
    card = relationship("SellerCard", backref="seller",
                        cascade="all,delete")
    notifications = relationship("SellerNotification", backref="seller",
                                 cascade="all,delete")

    def __init__(self, **kwargs):
        """Initializes the Seller Object."""
        # Add salt and hash password
        salt = uuid4().hex
        password = kwargs.get("password")
        password = sha256("{}{}".format(password, salt).
                          encode('utf-8')).hexdigest()
        kwargs.update({"password": password, "salt": salt})

        super().__init__(**kwargs)
