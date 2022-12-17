#!/usr/bin/python3
""" Subcategory class module
        Definition of SubCategory class, it attributes,
        and methods
"""
from sqlalchemy.orm import relationship
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Text
from models.base_model import Base, BaseModel


class SubCategory(Base, BaseModel):
    """Creates a Subcategory table object."""
    category_id = Column(String(60), ForeignKey('categories.id'))
    subcatory_name = Column(String(128), nullable=False)
    subcategory_description = Column(Text(255), nullable=False)

    def __init__(self, **kwargs):
        """Instantiates SubCategory object."""

        super().__init__(**kwargs)
