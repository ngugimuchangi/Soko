#!/usr/bin/python3
""" OrderDetail class module
        Definition of OrderDetail class, it attributes,
        and methods
"""
from sqlalchemy import (Column, Float, ForeignKey,
                        Integer, String,)
from models.base_model import Base, BaseModel


class OrderDetail(BaseModel, Base):
    """ OrderDetail class representing order_details table
        Attributes:
            order_id (str): foreign key to order table's id field
            product_id (str): product's id
            product_name (str): product's name
            seller_id (str): seller's id
            price (str): price of product
            quantity (str): quanity of product
            fulfillment_status(str): tracking status options
                                     (pending, shipped, delivered)
            review_status(srt): product review status
                                (pending, reviewed)
            payment_status(str): seller payment status for ordered
                                 product(pending, paid)
    """
    __tablename__ = "order_details"

    order_id = Column(String(60), ForeignKey("orders.id"), nullable=False)
    product_id = Column(String(60), nullable=False)
    product_name = Column(String(128), nullable=False)
    seller_id = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    fullfilment_status = Column(String(60), default="pending", nullable=False)
    review_status = Column(String(60), default="pending", nullable=False)
    payment_status = Column(String(60), default="pending", nullable=False)
