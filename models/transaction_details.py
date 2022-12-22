#!/usr/bin/python3
""" TransactionDetail module
        Definition of TransactionDetail class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Float, ForeignKey, String


class TransactionDetail(Base, BaseModel):
    """ TransactionDetail class representing transactions_details table
        Attributes:
            order_id: foreign key to orders table's
                      id field
            order_details_id (str): link to order details
            amount (float): amount paid to seller product delivered
    """
    __tablename__ = "transactions_details"

    order_id = Column(String(60), ForeignKey("orders.id"))
    order_detail_id = Column(String(60), nullable=False)
    amount = Column(Float, nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a TransactionDetail object."""
        super().__init__(**kwargs)
