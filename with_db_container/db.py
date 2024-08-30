"""
This module starts the database
"""

from sqlalchemy import create_engine
from dotenv import dotenv_values
from .models import Base

db_config = dotenv_values("app/.env")

DATABASE_URL = (
    f"mysql://"
    f"{db_config["USER"]}:{db_config["PSWD"]}"
    f"@{db_config["HOST"]}:{db_config["PORT"]}"
    f"/{db_config["NAME"]}"
)

engine = create_engine(DATABASE_URL)
# create the table and the schema
Base.metadata.create_all(engine)
