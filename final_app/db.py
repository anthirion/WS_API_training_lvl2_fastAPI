"""
This module starts the database
"""

from sqlalchemy import create_engine
# from dotenv import dotenv_values
from .models import Base

# db_config = dotenv_values("/home/anthirion/app/.env")
# db_config = dotenv_values(".env")

db_config = {
    "HOST": "34.76.26.208",
    "USER": "admin",
    "PORT": "3306",
    "PSWD": "WavestoneApiTraining",
    "NAME": "api_training",
}

user = db_config["USER"]
pswd = db_config["PSWD"]
host = db_config["HOST"]
port = db_config["PORT"]
name = db_config["NAME"]

DATABASE_URL = f"mysql://{user}:{pswd}@{host}:{port}/{name}"

engine = create_engine(DATABASE_URL)
# create the table and the schema
Base.metadata.create_all(engine)
