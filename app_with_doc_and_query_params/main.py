from fastapi import FastAPI, HTTPException
from typing import List
from .resources import all_products, all_users, all_orders


# start the API server
app = FastAPI()

products_next_id = len(all_products) + 1
users_next_id = len(all_users) + 1
orders_next_id = len(all_orders) + 1


@app.get("/")
async def welcome():
  return "Welcome to the API training"


@app.get("/products")
# TODO: Declare query parameters for name and category (you can declare other parameters if you want)
async def get_all_products():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api
@app.get("/products/{product_id}")
async def get_product_by_id():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.post("/products")
async def add_product():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.put("/products/{product_id}")
async def modify_product():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.delete("/products/{product_id}")
async def delete_product():
  pass


"""
Define all endpoints relative to user below
"""


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.get("/admin/users")
async def get_all_users():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.get("/admin/users/{user_id}")
async def get_user_by_id():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.post("/users")
async def add_user():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.put("/admin/users/{user_id}")
async def modify_user():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.delete("/admin/users/{user_id}")
async def delete_user():
  pass


"""
Define all endpoints relative to orders below
"""


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.get("/admin/orders")
async def get_all_orders():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.get("/admin/orders/{order_id}")
async def get_order_by_id():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.post("/admin/orders")
async def add_order():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.put("/admin/orders/{order_id}")
async def modify_order():
  pass


# TODO: add parameters to the decorator in order to improve the documentation of the api


@app.delete("/admin/orders/{order_id}")
async def delete_order():
  pass
