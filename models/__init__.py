"""
    Init file for models package
    Specification for module to import
"""
from models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()
