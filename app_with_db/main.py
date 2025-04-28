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
async def get_all_products(product_name: str = "", product_category: str = "") -> List[schemas.Product]:
  # start a session to make requests to the database
  with Session(engine) as session:
    try:
      if product_name:
        """ Retrieve all elements of name "name" if the name parameter is declared  """
        query = (
            select(models.Product)
            .where(models.Product.product_name == product_name)
        )
        return [session.execute(query).scalar_one()]
      elif product_category:
        """ Retrieve all elements of category "category" if the category parameter is declared  """
        query = (
            select(models.Product)
            .where(models.Product.category == product_category)
        )
        return [session.execute(query).scalar_one()]
      else:
        """ Retrieve all products if no parameter is declared  """
        query = select(models.Product)
        return session.execute(query).scalars().all()
    # manage error in case no product was found
    except exc.NoResultFound:
      # no product found in the db
      return {}


# TODO: add parameters to the decorator in order to improve the documentation of the api
@app.get("/products/{productId}")
async def get_product_by_id():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.post("/products")
async def add_product():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.put("/products/{productId}")
async def modify_product():
  # TODO
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.delete("/products/{productId}")
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
