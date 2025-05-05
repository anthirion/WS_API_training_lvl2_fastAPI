"""
This module starts the database
"""

from sqlalchemy import create_engine, URL
import os
from .models import Base

user = os.environ["USER"]
pswd = os.environ["PSWD"]
protocol = os.environ["PROTOCOL"]
host = os.environ["HOST"]
port = os.environ["PORT"]
db_name = os.environ["DB_NAME"]

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};" +
    f"Server={protocol}:{host},{port};"
    f"Database={db_name};"
    f"Uid={user};"
    f"Pwd={pswd};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

connection_url = URL.create(
    "mssql+pyodbc", query={"odbc_connect": connection_string}
)

engine = create_engine(connection_url, pool_pre_ping=True)
# create the table and the schema
Base.metadata.create_all(engine)
