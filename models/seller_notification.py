#!/usr/bin/python3
""" SellerNotification class module
        Definition of SellerNotification class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, String, Text


class SellerNotification(BaseModel, Base):
    """ SellerNotification class representing seller_notifications table
        Attributes:
                seller_id (str): foreign key to sellers table's
                                 id field
                message (str):  notification message
                read_status (str):  notification status
    """
    __tablename__ = "seller_notifications"

    seller_id = Column(String(60), ForeignKey("sellers.id"),
                       nullable=False)
    message = Column(Text, nullable=False)
    read_status = Column(Boolean, default=False, nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a SellerNotification object."""
        super().__init__(**kwargs)
