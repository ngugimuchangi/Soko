#!/usr/bin/python3
""" Subcategory class module
        Definition of SubCategory class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Subcategory(BaseModel, Base):
    """ Subcategory class representing subcategories table
        Attributes:
            category_id (str): foreign key to categories table's
                         id field
            subcategory_name (str): name of subcategory
            subcategory_description (str): description of subcategory
    """
    __tablename__ = "subcategories"

    category_id = Column(String(60), ForeignKey('categories.id'))
    subcategory_name = Column(String(128), nullable=False)
    subcategory_description = Column(Text, nullable=False)
    products = relationship("Product", backref="subcategory",
                            cascade="all,delete")

    def __init__(self, **kwargs):
        """Instantiates Subcategory object."""
        super().__init__(**kwargs)
