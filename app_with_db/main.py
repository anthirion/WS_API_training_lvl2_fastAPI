# imports for API operation
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, exc, func
from typing import List

from . import models, schemas
from .schemas import ErrorMessage
from .db import engine


"""
Start the api server
"""
app = FastAPI()

"""
Define all endpoints relative to products below
"""


@app.get("/")
async def welcome():
  return "Welcome to the API training"


@app.get("/products",
         description="Retourne un tableau JSON contenant les produits avec leurs détails",
         response_description="	Liste des produits",
         )
# example of product_name parameter usage:
# http://127.0.0.1:8000/products?product_name=Cafe Gourmet
# do not use double quotes or simple quotes
async def get_all_products(product_name: str = "",
                           product_category: str = "",
                           min_stock: int = 0,
                           min_price: float = 0,
                           max_price: float = float('inf'),
                           ) -> List[schemas.Product]:
  # start a session to make requests to the database
  with Session(engine) as session:
    try:
      if max_price < min_price:
        raise HTTPException(
            status_code=400,
            detail="max_price parameter must be superior than min_price"
        )
      if max_price < 0 or min_price < 0:
        raise HTTPException(
            status_code=400,
            detail="Prices must be positive"
        )
      if min_stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Stock parameter must be positive"
        )
      query = select(models.Product)
      if product_name:
        query = query.where(models.Product.product_name == product_name)
      if product_category:
        query = query.where(models.Product.category == product_category)
      query = query.where(models.Product.stock >= min_stock)
      query = query.where(models.Product.price >= min_price)
      query = query.where(models.Product.price <= max_price)

      return session.execute(query).scalars().all()
    # manage error in case no product was found
    except exc.NoResultFound:
      # no product found in the db
      return {}


# TODO: add parameters to the decorator in order to improve the documentation of the api
@app.get("/products/{product_id}")
async def get_product_by_id():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.post("/products")
async def add_product():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.put("/products/{product_id}")
async def modify_product():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.delete("/products/{product_id}")
async def delete_product():
  # TODO
  pass


"""
Define all endpoints relative to user below
"""


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.get("/admin/users")
async def get_all_users():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.get("/admin/users/{user_id}")
async def get_user_by_id():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.post("/users")
async def add_user():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.put("/admin/users/{user_id}")
async def modify_user():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.delete("/admin/users/{user_id}")
async def delete_user():
  # TODO
  pass


"""
Define all endpoints relative to orders below
"""


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.get("/admin/orders")
async def get_all_orders():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.get("/admin/orders/{order_id}")
async def get_order_by_id():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.post("/admin/orders")
async def add_order():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.put("/admin/orders/{order_id}")
async def modify_order():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.delete("/admin/orders/{order_id}")
async def delete_order():
  # TODO
  pass
