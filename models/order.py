#!/usr/bin/python3
""" Order class module
        Definition of Order class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Float, String, Text
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """ Order class representing orders table
        Attributes:
            customer_id: customer who made the order
            subtotal (int): total cost of all producst before
                            vat and shipping cost
            vat: (int): vat charged
            shipping_cost(int): shipping cost
            shipping_address(str): shipping address
            order_status(int): order completion status (options:
                                awaiting payment, paid, completed)
            order_details: relationship with order detail's table
            transactions: relationship with transaction's table
    """
    __tablename__ = "orders"

    customer_id = Column(String(60), nullable=True)
    subtotal = Column(Float, nullable=False)
    vat = Column(Float,nullable=False)
    shipping_cost = Column(Float, nullable=False)
    shipping_address = Column(Text, nullable=True)
    order_status = Column(String(60), default="awating payment",
                          nullable=False)
    details = relationship("OrderDetail", backref="order",
                           cascade="all,delete")
    transactions = relationship("Transaction", backref="order",
                                cascade="all,delete")

    def __init__(self, **kwargs):
        """Instantiates the Order object."""
        super().__init__(**kwargs)
