#!/usr/bin/python3
""" Review class module
        Definition of Review class, it attributes,
        and methods
"""
from sqlalchemy.orm import relationship
import models
from os import getenv
from sqlalchemy import Column, String, Integer, ForeignKey, Text


from models.base_model import Base, BaseModel


class Review (Base, BaseModel):
    """Creates A Review table object."""
    buyer_id = Column(String(60), ForeignKey('buyers.id'))
    product_id = Column(String(60), ForeignKey('products.id'))
    rating = Column(Integer)
    review = Column(Text(255), nullable=True)

    def __init__(self, *args, **kwargs):
        """Instantiates a Review object."""

        super().__init__(*args, **kwargs)
