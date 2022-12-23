#!/usr/bin/python3
""" TransactionDetail module
        Definition of TransactionDetail class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Float, ForeignKey, String


class TransactionDetail(BaseModel, Base):
    """ TransactionDetail class representing transactions_details table
        Attributes:
            transaction_id: foreign key to transactions table's
                            id field
            order_details_id (str): link to order details
            amount (float): amount paid to seller product delivered
    """
    __tablename__ = "transaction_details"

    transaction_id = Column(String(60), ForeignKey("transactions.id"))
    order_detail_id = Column(String(60), nullable=False)
    amount = Column(Float, nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a TransactionDetail object."""
        super().__init__(**kwargs)
