"""
    Init file for models package
    Specification for module to import
"""
from dotenv import load_dotenv
from models.engine.db_storage import DBStorage

storage = DBStorage()
