#!/usr/bin/python3
""" Product class module
        Definition of Product class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import (Column,ForeignKey, Integer,
                        Numeric, String, Text)
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """ Product class representing products table
        Attributes:
            product_name (str): Name of the product
            category_id (str): foreign key to subcategories table's
                               id field
            seller_id (str): foreign key to sellers table's
                             id field
            product_description (text): long description of product
            stock(int): amount of product in stock
            images: relationship with product_images table
            reviews: relationship with reviews table
    """
    __tablename__ = "products"

    product_name = Column(String(128), nullable=False)
    category_id = Column(String(60), ForeignKey('subcategories.id'))
    seller_id = Column(String(60), ForeignKey('sellers.id'))
    product_description = Column(Text, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    images = relationship("ProductImage", backref="product",
                          cascade="all,delete")
    reviews = relationship("Review", backref="product",
                           cascade="all,delete")

    def __init__(self, **kwargs):
        """Instantiates Product object."""
        super().__init__(**kwargs)
