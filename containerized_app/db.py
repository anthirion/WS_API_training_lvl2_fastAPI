"""
This module starts the database
"""

from sqlalchemy import create_engine
import os
from .models import Base

user = os.environ["USER"]
pswd = os.environ["PSWD"]
host = os.environ["HOST"]
port = os.environ["PORT"]
name = os.environ["NAME"]

DATABASE_URL = f"mysql://{user}:{pswd}@{host}:{port}/{name}"

engine = create_engine(DATABASE_URL)
# create the table and the schema
Base.metadata.create_all(engine)
