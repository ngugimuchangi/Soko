#!/usr/bin/python3
""" Category class module
        Definition of Category class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Text


class Category(BaseModel, Base):
    """ Category class representing categories table
        Attributes:
            category_name: category's name
            category_description: category's description
            subcategories: relationship with subcategories
                           field
    """
    __tablename__ = "categories"

    category_name = Column(String(128), nullable=False)
    category_description = Column(Text, nullable=False)
    subcategories = relationship("Subcategory", backref="category",
                                 cascade="all,delete")

    def __init__(self, **kwargs):
        """Instantiates the Category object."""
        super().__init__(**kwargs)
