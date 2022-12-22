#!/usr/bin/python3
""" Transaction module
        Definition of Transaction class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Transaction(BaseModel, Base):
    """ Transaction class representing transactions table
        Attributes:
            seller_id: seller's id
            order_id: foreign key to orders table's
                      id field
            amount: amount paid to seller
            details: relationship with transaction_details table
    """
    __tablename__ = "transactions"

    seller_id = Column(String(60), nullable=False)
    order_id = Column(String(60), ForeignKey("orders.id"))
    amount = Column(Float, nullable=False)
    details = relationship("TransactionDetail", backref="transaction",
                           cascade="all,delete")

    def __init__(self, **kwargs):
        """Instantiates a Transaction object."""
        super().__init__(**kwargs)
