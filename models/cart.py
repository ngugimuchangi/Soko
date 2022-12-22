#!/usr/bin/python3
""" Cart class module
        Definition of Cart class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String


class Cart(BaseModel, Base):
    """ Cart class representing cart table
        Attributes:
                customer_id (str): foreign key to customer table's
                                   id field
                product_id (str):  product's id
                product_name (str):  product's name
                product_image (str) product's main image
                quantity (int): quantity of a particular item in cart
    """
    __tablename__ = "cart"

    customer_id = Column(String(60), ForeignKey("customers.id"),
                         nullable=False)
    product_id = Column(String(60), nullable=False)
    product_name = Column(String(128), nullable=False)
    product_image = Column(String(128), nullable=False)
    quantity = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a Cart object."""
        super().__init__(**kwargs)
