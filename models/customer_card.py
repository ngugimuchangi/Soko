#!/usr/bin/python3
""" Card class module
        Definition of Buyer class, it attributes,
        and methods
"""
from datetime import date
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, String, Date


class CustomerCard(BaseModel, Base):
    """ CustomerCard class representing customer_cards table
        Attributes:
            customer_id (str): foreign key to customer table's
                               id field
            card_number (str): card's number
            cvv (str):  card's cvv
            expiry_date(str):
            name_on_card (str): identity of card holder
            card_type (str): card_type

    """
    __tablename__ = "customer_cards"

    customer_id = Column(String(60), ForeignKey("customers.id"),
                         nullable=False)
    card_number = Column(String(60), nullable=False)
    cvv = Column(String(60), nullable=False)
    expiry_date = Column(Date, nullable=False)
    name_on_card = Column(String(128), nullable=False)
    card_type = Column(String(60), nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a CustomerCard object"""
        # Create date object for expiry date
        expiry_date = kwargs.get("expiry_date")
        month = expiry_date.get("month")
        year = expiry_date.get("year")
        expiry_date = date(year, month, 1)

        # Check card type
        card_number = str(kwargs.get("card_number"))
        if card_number.startswith("4"):
            card_type = "visa"
        elif card_number.startswith("5"):
            card_type = "mastercard"
        else:
            card_type = "other"

        kwargs.update({"expiry_date": expiry_date,
                      "card_type": card_type})
        super().__init__(**kwargs)
