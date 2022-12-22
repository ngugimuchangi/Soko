#!/usr/bin/python3
""" BuyerNotification class module
        Definition of BuyerNotification class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Text


class CustomerNotification(BaseModel, Base):
    """ CustomerNotification class representing customer_notifications table
        Attributes:
                customer_id (str): foreign key to customer table's
                                   id field
                message (str):  notification message
                read_status (int):  notification's status
    """
    __tablename__ = "customer_notifications"

    customer_id = Column(String(60), ForeignKey("customers.id"),
                         nullable=False)
    message = Column(Text, nullable=False)
    read_status = Column(Integer, default=0, nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a CustomerNotification object."""
        super().__init__(**kwargs)
