#!/usr/bin/python3
""" Chat class module
        Definition of Chat class, it attributes,
        and methods
"""
from sqlalchemy.orm import relationship
import models
from os import getenv
from sqlalchemy import Column, String, Integer, ForeignKey, Text


from models.base_model import Base, BaseModel


class Chat(Base, BaseModel):
    """Creates a Chat table object."""
    seller_id = Column(String(60), ForeignKey('sellers.id'))
    buyer_id = Column(String(60), ForeignKey('buyers.id'))
    buyer_status = Column(Integer, nullable=False)
    seller_status = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a Chat object."""

        super().__init__(**kwargs)
