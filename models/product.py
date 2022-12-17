#!/usr/bin/python3
""" Product class module
        Definition of Product class, it attributes,
        and methods
"""


import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Numeric, CheckConstraint, ForeignKey, Text
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class Product(Base, BaseModel):
    """Creates the Product table Object."""
    product_name = Column(String(128), nullable=False)
    categor_id = Column(Integer, ForeignKey('categories.id'))
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    order = relationship('Order', backref='order')
    review = relationship('Review', backref='review')
    quantity = Column(Integer, nullable=False)
    cost_per_unit = Column(Numeric(12, 2), nullable=False, CheckConstraint('cost_per_unit >= 0.00', name='unit_cost_positive'))
    product_description = Column(Text, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates Product Object."""

        super().__init__(*args, **kwargs)
