from fastapi import FastAPI, HTTPException
from typing import List

from .schemas import (
    Product, ProductBase,
    User, UserBase,
    Order, OrderBase,
)
from .resources import all_products, all_users, all_orders

# start the API server
app = FastAPI()

products_next_id = len(all_products) + 1
users_next_id = len(all_users) + 1
orders_next_id = len(all_orders) + 1


@app.get("/")
async def welcome():
  return "Welcome to the API training"


"""
Define all endpoints relative to product below
"""


@app.get("/products")
async def get_all_products() -> List[Product]:
  return all_products


@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int) -> Product:
  for product in all_products:
    if product.id == product_id:
      return product
  # if no product is found, raise an error
  raise HTTPException(status_code=404, detail="Produit introuvable")


@app.post("/products")
async def add_product(new_product: ProductBase) -> Product:
  global products_next_id
  """ Check that the product is not already in the database   """
  if new_product not in all_products:
    new_product = Product.add_id(new_product, products_next_id)
    products_next_id += 1
    all_products.append(new_product)
    return new_product
  else:
    raise HTTPException(status_code=409,
                        detail="Produit déjà existant")


@app.put("/products/{product_id}")
async def modify_product(product_id: int, new_product: ProductBase) -> Product:
  """ Search the given product in the database with its id  """
  for i, product in enumerate(all_products):
    if product.id == product_id:
      # add the id in the URL to the given product
      new_product_with_id = Product.add_id(new_product, product_id)
      all_products[i] = new_product_with_id
      return new_product_with_id
  raise HTTPException(status_code=404,
                      detail="Produit introuvable")


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
  global products_next_id
  """ Search the given product in the database with its id  """
  found = False
  for i, product in enumerate(all_products):
    if product.id == product_id:
      products_next_id = product.id
      del all_products[i]
      found = True
  if not found:
    raise HTTPException(status_code=404,
                        detail="Produit introuvable")


"""
Define all endpoints relative to user below
"""


@app.get("/admin/users")
async def get_all_users() -> List[User]:
  return all_users


@app.get("/admin/users/{user_id}")
async def get_user_by_id(user_id: int) -> User:
  for user in all_users:
    if user.id == user_id:
      return user
  # if no user is found, raise an error
  raise HTTPException(status_code=404, detail="Utilisateur introuvable")


@app.post("/users")
async def add_user(new_user: UserBase) -> User:
  global users_next_id
  """ Check that the user is not already in the database   """
  if new_user not in all_users:
    new_user = User.add_id(new_user, users_next_id)
    users_next_id += 1
    all_users.append(new_user)
    return new_user
  else:
    raise HTTPException(status_code=409,
                        detail="Utilisateur déjà existant")


@app.put("/admin/users/{user_id}")
async def modify_user(user_id: int, new_user: UserBase) -> User:
  """ Search the given user in the database with its id  """
  for i, user in enumerate(all_users):
    if user.id == user_id:
      # add the id in the URL to the given user
      new_user_with_id = User.add_id(new_user, user_id)
      all_users[i] = new_user_with_id
      return new_user_with_id
  raise HTTPException(status_code=404,
                      detail="Utilisateur introuvable")


@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: int):
  global users_next_id
  """ Search the given user in the database with its id  """
  found = False
  for i, user in enumerate(all_users):
    if user.id == user_id:
      users_next_id = user.id
      del all_users[i]
      found = True
  if not found:
    raise HTTPException(status_code=404,
                        detail="Utilisateur introuvable")


"""
Define all endpoints relative to orders below
"""


@app.get("/admin/orders")
async def get_all_orders() -> List[Order]:
  return all_orders


@app.get("/admin/orders/{order_id}")
async def get_order_by_id(order_id: int) -> Order:
  for order in all_orders:
    if order.id == order_id:
      return order
  # if no order is found, raise an error
  raise HTTPException(status_code=404, detail="Commande introuvable")


@app.post("/admin/orders")
async def add_order(new_order: OrderBase) -> Order:
  global orders_next_id
  """ Check that the order is correct and is not already in the database   """
  if new_order not in all_orders:
    if new_order.is_correct(all_products) is False:
      raise HTTPException(status_code=400,
                          detail="Commande incorrecte")
    else:
      new_order = Order.add_id(new_order, orders_next_id)
      orders_next_id += 1
      all_orders.append(new_order)
      return new_order
  else:
    raise HTTPException(status_code=409,
                        detail="Commande déjà existante")


@app.put("/admin/orders/{order_id}")
async def modify_order(order_id: int, new_order: OrderBase) -> Order:
  """ Search the given order in the database with its id  """
  if new_order.is_correct(all_products) is True:
    for i, order in enumerate(all_orders):
      if order.id == order_id:
        # add the id in the URL to the given order
        new_order_with_id = Order.add_id(new_order, order_id)
        all_orders[i] = new_order_with_id
        return new_order_with_id
  else:
    raise HTTPException(status_code=400,
                        detail="Commande incorrecte")
  raise HTTPException(status_code=404,
                      detail="Commande introuvable")


@app.delete("/admin/orders/{order_id}")
async def delete_order(order_id: int):
  global orders_next_id
  """ Search the given order in the database with its id  """
  found = False
  for i, order in enumerate(all_orders):
    if order.id == order_id:
      orders_next_id = order.id
      del all_orders[i]
      found = True
  if not found:
    raise HTTPException(status_code=404,
                        detail="Commande introuvable")
