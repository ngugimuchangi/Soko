#!/usr/bin/python3
""" Category class module
        Definition of Category class, it attributes,
        and methods
"""

from typing import Text
from sqlalchemy.orm import relationship
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Text
from models import subcategory
from models import product
from models.base_model import Base, BaseModel


class Category(Base, BaseModel):
    """Creates the Category table object."""
    category_name = Column(String(128), nullable=False)
    category_description = Column(Text(255), nullable=False)
    product = relationship('Product', backref='product')
    subcategory = relationship('Subcategory', backref='subcategory')

    def __init__(self, **kwargs):
        """Initializes the category object."""

        super().__init__(**kwargs)
