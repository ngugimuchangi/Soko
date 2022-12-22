#!/usr/bin/python3
""" ShippingAddresses class module
        Definition of ShippingAddress class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, Text


class ShippingAddress(BaseModel, Base):
    """ ShippingAddress class representing shipping_addresses table
        Attributes:
            customer_id: foreign key to customer table's
                         id field
            first_name: first_name of person associated with address
            last_name: last_name of person associated with address
            phone_number: last_name of person associated with address
            shipping_address: shipping address details
    """
    __tablename__ = "shipping_addresses"

    customer_id = Column(String(60), ForeignKey('customers.id'))
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone_number = Column(String(60), nullable=False)
    shipping_address = Column(Text, nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a ShippingAddress object."""
        super().__init__(**kwargs)
