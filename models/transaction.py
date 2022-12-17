#!/usr/bin/python3
""" Base Trasnaction module
        Definition of Base class, it attributes,
        and methods
"""
from sqlalchemy.orm import relationship
import models
from os import getenv
from sqlalchemy import Column, String, ForeignKey,


from models.base_model import Base, BaseModel


class Transaction(Base, BaseModel):
    """Creates a Transaction table object."""
    order_id = Column(String(60), ForeignKey('orders.id'))

    def __init__(self, *args, **kwargs):
        """Instantiates a Transaction object."""

        super().__init__(*args, **kwargs)
