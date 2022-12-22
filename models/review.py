#!/usr/bin/python3
""" Review class module
        Definition of Review class, it attributes,
        and methods
"""

from sqlalchemy import (Column, ForeignKey,
                        Integer, String, Text)
from models.base_model import Base, BaseModel


class Review (BaseModel, Base):
    """ Review class representing reviews table
        Attributes:
            first_name (str): customer's first name
            last_name (str): customer's last name
            product_id (str): foreign key to product id table
            rating (int): product rating
            review (text): customer's review
    """
    __tablename__ = "reviews"

    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'))
    rating = Column(Integer, nullable=False)
    review = Column(Text(255), nullable=True)

    def __init__(self, *args, **kwargs):
        """Instantiates a Review object."""

        super().__init__(*args, **kwargs)
