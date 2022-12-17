#!/usr/bin/python3
""" ShippingAddresses class module
        Definition of ShippingAddress class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship

import models
from os import getenv
from sqlalchemy import Column, String, Integer, Numeric, CheckConstraint, ForeignKey, Text


class ShippingAddress(Base, BaseModel):
    """Creates a ShippingAddress table Object."""
    buyer_id = Column(String(60), ForeignKey('buyers.id'))
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone_number = Column(String(20), nullable=False)
    shipping_address = Column(Text, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiate a ShippingAddress object."""

        super().__init__(*args, **kwargs)
