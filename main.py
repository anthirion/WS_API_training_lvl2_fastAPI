# imports for API operation
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

# import list of products and ProductBase class
from . import models
from .db import engine, Base

"""
Start the api server
"""
app = FastAPI()

"""
Configure the database
"""
# create the product table in the database
Base.metadata.create_all(engine)

"""
Define endpoints below
"""


@app.get("/products")
def get_all_products():
    with Session(engine) as session:
        products = select(models.Product)
        if products is None:
            raise HTTPException(status_code=404, detail="No product found")
        return [product for product in session.scalars(products)]
