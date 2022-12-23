#!/usr/bin/python3
""" Order class module
        Definition of Order class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import (Column, CheckConstraint,
                        Float, String, Text)
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
            order_status(int): order completeion status (options:
                                awaiting payment, paid, completed)
            order_details: relationship with order detail's table
            transactions: relationship with transaction's table
    """
    __tablename__ = "orders"

    customer_id = Column(String(60), nullable=True)
    subtotal = Column(Float, CheckConstraint('subtotal > 0',
                      name='subtotal_positive'),
                      nullable=False)
    vat = Column(Float, CheckConstraint('vat > 0',
                 name='vat_positive'),
                 nullable=False)
    shipping_cost = Column(Float, CheckConstraint('shipping_cost > 0.00',
                           name='shipping_cost_positive'), nullable=False)
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
