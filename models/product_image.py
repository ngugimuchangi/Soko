#!/usr/bin/python3
""" ProductImage class module
        Definition of ProductImage class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey,  String


class ProductImage(BaseModel, Base):
    """ ProductImage class represent product_images table
        Attributes:
            product_id (str): foreign key to products table
                              id field
            file_path (str): absolute path of the image
            status(str): image status, whether default or not
    """
    __tablename__ = "product_images"

    products_id = Column(String(60), ForeignKey("products.id"),
                         nullable=False)
    file_path = Column(String(256), nullable=False)
    status = Column(String(60), nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a ProductImage object"""
        super().__init__(**kwargs)
