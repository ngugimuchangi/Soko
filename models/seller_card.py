#!/usr/bin/python3
""" SellerCard class module
        Definition of SellerCard class, it attributes,
        and methods
"""
from datetime import date
from flask_login import UserMixin
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Date, ForeignKey, String


class SellerCard(BaseModel, Base, UserMixin):
    """ SellerCard class representing seller_cards table
        Attributes:
            seller_id (str): foreign key to seller table's
                             id field
            card_number (str): card's number
            cvv (str):  card's cvv
            expiry_date(str):
            name_on_card (str): identity of card holder
            card_type (str): card_type
    """
    __tablename__ = "seller_cards"

    seller_id = Column(String(60), ForeignKey("sellers.id"),
                       nullable=False)
    card_number = Column(String(60), nullable=False)
    cvv = Column(String(60), nullable=False)
    expiry_date = Column(Date, nullable=False)
    name_on_card = Column(String(128), nullable=False)
    card_type = Column(String(60), nullable=False)

    def __init__(self, **kwargs):
        """Instantiates a SellerCard object"""
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
