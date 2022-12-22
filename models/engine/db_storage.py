#!/usr/bin/python3
""" Database storage engine module
"""
from dotenv import load_dotenv
from models.base_model import Base
from models.cart import Cart
from models.category import Category
from models.chat import Chat
from models.customer import Customer
from models.customer_card import CustomerCard
from models.customer_notification import CustomerNotification
from models.customer import Customer
from models.message import Message
from models.order_detail import OrderDetail
from models.order import Order
from models.product import Product
from models.product_image import ProductImage
from models.review import Review
from models.saved_item import SavedItem
from models.seller_card import SellerCard
from models.seller_notification import SellerNotification
from models.seller import Seller
from models.shipping_address import ShippingAddress
from models.subcategory import Subcategory
from models.transaction import Transaction
from models.transaction_details import TransactionDetail
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()


class DBStorage():
    """ Database engine class for interacting with the msql database"""
    __engine = None
    __session = None

    def __init__(self):
        """ Constructor method to create engine for database storage"""
        # environment variables
        env = getenv("SOKO_ENV")
        user = getenv("SOKO_MYSQL_USER")
        pwd = getenv("SOKO_MYSQL_PWD")
        host = getenv("SOKO_MYSQL_HOST")
        db = getenv("SOKO_MYSQL_DB")
        if all(var is not None for var in [user, pwd, host, db]):
            self.__engine = create_engine("{}://{}:{}@{}/{}".format(
                            "mysql+mysqldb", user, pwd, host, db),
                            pool_pre_ping=True)
            if env == 'test':
                # delete all tables
                Base.metadata.drop_all(bind=self.__engine)

    @property
    def session(self):
        """ Getter method for session
        """
        return self.__session

    def search(self, cls=None, id=None):
        """ Queries current database session for all objects
            belonging to a specific class if provided, else
            all objects for every class
            Args:
                cls: class of objects to return
            Return:  a list of objects found or obj itself if
                     search criteria include obj id and class
                     else None
        """
        class_list = [Customer, CustomerNotification, CustomerCard,
                      Cart, Category, Chat, Order,
                      OrderDetail, Product, ProductImage, Message,
                      Review, SavedItem, SellerNotification, SellerCard,
                      Seller, ShippingAddress,
                      Subcategory, Transaction, TransactionDetail]
        objs = []

        if cls is not None and id is None:
            # query for all records in particular table
            # Add them to dictionary 'objs'

            objs = list(self.__session.query(cls).all())
            return objs
        elif cls is None and id is None:
            # query for all objects in all tables
            # Add them to dictionary 'objs'
            objs = []
            for cl in class_list:
                for obj in self.__session.query(cl).all():
                    objs.append(obj)
            return objs
        else:
            obj = self.__session.query(cls).filter_by(id=id).first()
            return obj

        return objs

    def new(self, obj):
        """ Adds item to current database session
            Args:
                obj: object to add
            Return: Nothing
        """
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete objects from current database """
        if obj is not None:
            # check if object exists in table before deleting it
            obj_query = self.__session.query(obj.__class__).filter_by(
                    id=obj.id).one_or_none()
            if obj_query is not None:
                self.__session.delete(obj_query)
                self.save()

    def reload(self):
        """ Create all tables in the database
            Args: None
            Return: Nothing
        """
        # create all tables
        Base.metadata.create_all(self.__engine)

        # create session
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """closes the session"""
        self.__session.close()
