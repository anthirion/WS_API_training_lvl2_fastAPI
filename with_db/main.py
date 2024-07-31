# imports for API operation
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from typing import List

# import list of products and ProductBase class
from . import models, schemas
from .db import engine, Base

"""
Start the api server
"""
app = FastAPI()

"""
Define endpoints
"""


@app.get("/")
def welcome():
    return "Welcome to the API training"


@app.get("/products")
def get_all_products() -> List[schemas.Product]:
    with Session(engine) as session:
        try:
            query = select(models.Product)
            products = session.execute(query).scalars().all()
        # manage error in case no product was found
        except exc.NoResultFound:
            raise HTTPException(status_code=404,
                                detail="No product found")
        return [product for product in products]


@app.get("/products/{product_id}")
def get_product(product_id: int):
    with Session(engine) as session:
        try:
            query = (
                select(models.Product)
                .where(models.Product.id == int(product_id))
            )
            product = session.execute(query).scalar_one()
        # manage error in case no product was found
        except exc.NoResultFound:
            raise HTTPException(status_code=404,
                                detail=f"No product with id {product_id} found")
        return product
