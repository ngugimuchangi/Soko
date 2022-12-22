#!/usr/bin/python3
""" Message class module
        Definition of Message class, it attributes,
        and methods
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, String, Text


class Message(Base, BaseModel):
    """ Message class representing messages table
        Attributes:
            chat_id (str): foreign key to chats table's
                           id field
            sender (str): message sender
            receiver (str): message receiver
            message_type(str): type of message sent. (file, text, or both)
            message (text): text message if any
            file_path (str): path to file if any
    """
    __tablename__ = "messages"

    chat_id = Column(String(60), ForeignKey("chats.id"))
    sender = Column(String(60), nullable=False)
    receiver = Column(String(60), nullable=False)
    message_type = Column(String(60), nullable=False)
    message = Column(Text, nullable=True)
    file_path = Column(String(128), nullable=True)

    def __init__(self, **kwargs):
        """Instantiates a new Message object"""
        super().__init__(**kwargs)
