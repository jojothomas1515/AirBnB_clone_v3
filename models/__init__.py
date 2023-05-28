#!/usr/bin/python3
"""
initialize the models package
"""

from load_env import load_env_file
from os import getenv

load_env_file()

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
