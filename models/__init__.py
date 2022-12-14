"""
    Init file for models package
    Specification for module to import
"""
from dotenv import load_dotenv
from models.engine.db_storage import DBStorage
from os import getenv

load_dotenv()

if getenv('SOKO_TYPE_STORAGE') == 'db_storage':
    storage = DBStorage()