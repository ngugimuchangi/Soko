#!/usr/bin/python3
""" Order class module
        Definition of Order class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import (Column, String, Integer, Numeric,
                        CheckConstraint, ForeignKey)
from sqlalchemy.orm import relationship


class Order(Base, BaseModel):
    """Creates the Order table Object."""

    order_type = Column(String(60), nullable=False)
    order_status = Column(String(60), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Numeric(12, 2), CheckConstraint('unit_cost >= 0.00',
                       name='unit_cost_positive'), nullable=False)
    payment_method = Column(String(60), nullable=False, unique=True)
    review_status = Column(String(60), nullable=True)
    product_id = Column(String(60), ForeignKey('products.id'))
    buyer_id = Column(String(60), ForeignKey('buyers.id'))
    transaction = relationship('Transaction', backref='transaction')

    def __init__(self, *args, **kwargs) -> None:
        """Instantiates the Order object."""

        super().__init__(*args, **kwargs)
