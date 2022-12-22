#!/usr/bin/python3
""" Chat class module
        Definition of Chat class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Chat(BaseModel, Base):
    """Creates a Chat table object."""

    __tablename__ = "chats"

    seller_id = Column(String(60), ForeignKey('sellers.id'))
    customer_id = Column(String(60), ForeignKey('customers.id'))
    customer_read_status = Column(Integer, default=0, nullable=False)
    seller_read_status = Column(Integer, default=0, nullable=False)
    customer_delete_status = Column(Integer, default=0, nullable=False)
    seller_delete_status = Column(Integer, default=0, nullable=False)
    messages = relationship("Message", backref="chat", cascade="all,delete")

    def __init__(self, **kwargs):
        """Instantiates a Chat object."""
        super().__init__(**kwargs)
