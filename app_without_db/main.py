from fastapi import FastAPI, HTTPException
from typing import List
from .schemas import Product, ProductBase
from .resources import all_products

# start the API server
app = FastAPI()


@app.get("/")
async def welcome():
  return "Welcome to the API training"


"""
Define all endpoints relative to product below
"""


@app.get("/products")
async def get_all_products() -> List[Product]:
  return all_products


@app.get("/products/{productId}")
async def get_product_by_id(productId: int) -> Product:
  # TODO
  pass


@app.post("/products")
async def add_product(new_product: ProductBase) -> Product:
  # TODO
  pass


@app.put("/products/{productId}")
async def modify_product(productId: int, new_product: ProductBase) -> Product:
  # TODO
  pass


@app.delete("/products/{productId}")
async def delete_product(productId: int):
  # TODO
  pass


"""
Define all endpoints relative to user below
"""


@app.get("/admin/users")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def get_all_users():
  pass


@app.get("/admin/users/{user_id}")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def get_user_by_id():
  pass


@app.post("/users")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def add_user():
  pass


@app.put("/admin/users/{user_id}")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def modify_user():
  pass


@app.delete("/admin/users/{user_id}")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def delete_user():
  pass


"""
Define all endpoints relative to orders below
"""


@app.get("/admin/orders")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def get_all_orders():
  pass


@app.get("/admin/orders/{order_id}")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def get_order_by_id():
  pass


@app.post("/admin/orders")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def add_order():
  pass


@app.put("/admin/orders/{order_id}")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def modify_order():
  pass


@app.delete("/admin/orders/{order_id}")
# TODO: add necessary parameters to the function (use examples of products endpoints)
async def delete_order():
  pass
