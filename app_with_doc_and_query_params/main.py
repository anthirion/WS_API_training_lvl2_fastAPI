from fastapi import FastAPI, HTTPException
from typing import List

from .resources import all_products, all_users, all_orders
from .schemas import (
    ProductBase, Product,
    User, UserBase,
    Order, OrderBase,
    ErrorMessage
)

# start the API server
app = FastAPI()

products_next_id = len(all_products) + 1
users_next_id = len(all_users) + 1
orders_next_id = len(all_orders) + 1


@app.get("/")
async def welcome():
  return "Welcome to the API training"


@app.get("/products",
         description="Retourne un tableau JSON contenant les produits avec leurs détails",
         # response_description is the description to display when no error occured (code 200)
         response_description="	Liste des produits",
         )
# Declare query parameters for name and category (you can declare other parameters if you want)
# WARNING: Do NOT add quotes for query parameters -> products?category=Alimentation
async def get_all_products(product_name: str = "",
                           product_category: str = "",
                           min_stock: int = 0,
                           min_price: float = 0,
                           max_price: float = float('inf'),
                           ) -> List[Product]:
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
  requested_products = set(all_products)
  select_products_by_name = set(all_products)
  select_products_by_category = set(all_products)
  if product_name:
    select_products_by_name = set(
        [product for product in all_products if product.product_name == product_name])
  if product_category:
    select_products_by_category = set(
        [product for product in all_products if product.category == product_category])
  select_products_by_stock = set(
      [product for product in all_products if product.stock >= min_stock])
  select_products_by_min_price = set(
      [product for product in all_products if product.price >= min_price])
  select_products_by_max_price = set(
      [product for product in all_products if product.price <= max_price])
  return requested_products.intersection(select_products_by_name,
                                         select_products_by_category,
                                         select_products_by_stock,
                                         select_products_by_min_price,
                                         select_products_by_max_price,
                                         )


@app.get("/products/{product_id}",
         description="Retourne un objet JSON contenant les détails d'un produit spécifique",
         response_description="	Détails du produit",
         # responses enables you to async define additional responses code and message
         # the async default code responses are 200 and 422
         responses={404: {"model": ErrorMessage,
                          "description": "Produit introuvable"}},
         )
async def get_product_by_id(product_id: int) -> Product:
  for product in all_products:
    if product.id == product_id:
      return product
  # if no product is found, raise an error
  raise HTTPException(status_code=404, detail="Produit introuvable")


@app.post("/products",
          description="Ajouter un nouveau produit",
          response_description="Produit ajouté",
          # status code async defines the status code to return when no error occured
          # since this operation is a creation, return 201 instead of 200
          status_code=201,
          responses={409: {"model": ErrorMessage,
                           "description": "Produit déjà existant"}},
          )
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


@app.put("/products/{product_id}",
         description="Modifier un produit existant",
         response_description="Produit mis à jour",
         responses={404: {"model": ErrorMessage,
                          "description": "Produit introuvable"}},
         )
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


@app.delete("/products/{product_id}",
            description="Supprimer un produit",
            response_description="Produit supprimé",
            status_code=204,
            responses={404: {"model": ErrorMessage,
                             "description": "Produit introuvable"}},
            )
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


@app.get("/admin/users",
         description="Retourne un tableau JSON contenant les utilisateurs avec leurs détails",
         response_description="	Liste des utilisateurs",
         )
async def get_all_users(name: str = "",
                        email: str = "",
                        ) -> List[User]:
  requested_users = set(all_users)
  select_users_by_name = set(all_users)
  select_users_by_email = set(all_users)
  if name:
    select_users_by_name = set(
        [user for user in all_users if user.username == name])
  if email:
    select_users_by_email = set(
        [user for user in all_users if user.email == email])
  return requested_users.intersection(select_users_by_name,
                                      select_users_by_email,
                                      )


@app.get("/admin/users/{user_id}",
         description="Retourne un objet JSON contenant les détails d'un utilisateur spécifique",
         response_description="	Détails de l'utilisateur",
         responses={404: {"model": ErrorMessage,
                          "description": "Utilisateur introuvable"}},
         )
async def get_user_by_id(user_id: int) -> User:
  for user in all_users:
    if user.id == user_id:
      return user
  # if no user is found, raise an error
  raise HTTPException(status_code=404, detail="Utilisateur introuvable")


@app.post("/users",
          description="Ajouter un nouveau utilisateur",
          response_description="Utilisateur ajouté",
          status_code=201,
          responses={409: {"model": ErrorMessage,
                           "description": "Utilisateur déjà existant"}},
          )
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


@app.put("/admin/users/{user_id}",
         description="Modifier un utilisateur existant",
         response_description="Utilisateur mis à jour",
         responses={404: {"model": ErrorMessage,
                          "description": "Utilisateur introuvable"}},
         )
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


@app.delete("/admin/users/{user_id}",
            description="Supprimer un utilisateur",
            response_description="Utilisateur supprimé",
            status_code=204,
            responses={404: {"model": ErrorMessage,
                             "description": "Utilisateur introuvable"}},
            )
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


@app.get("/admin/orders",
         description="Retourne un tableau JSON contenant les commandes avec leurs détails",
         response_description="	Liste des commandes",
         )
async def get_all_orders() -> List[Order]:
  return all_orders


@app.get("/admin/orders/{order_id}",
         description="Retourne un objet JSON contenant les détails d'une commande spécifique",
         response_description="	Détails de la commande",
         responses={404: {"model": ErrorMessage,
                          "description": "Commande introuvable"}},
         )
async def get_order_by_id(order_id: int) -> Order:
  for order in all_orders:
    if order.id == order_id:
      return order
  # if no order is found, raise an error
  raise HTTPException(status_code=404, detail="Commande introuvable")


@app.post("/admin/orders",
          description="Ajouter une nouvelle commande",
          response_description="Commande ajoutée",
          status_code=201,
          responses={409: {"model": ErrorMessage,
                           "description": "Commande déjà existante"},
                     400: {"model": ErrorMessage,
                           "description": "Commande incorrecte"}},
          )
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


@app.put("/admin/orders/{order_id}",
         description="Modifier une commande existante",
         response_description="Commande mise à jour",
         responses={404: {"model": ErrorMessage,
                          "description": "Commande introuvable"},
                    400: {"model": ErrorMessage,
                          "description": "Commande incorrecte"}},
         )
async def modify_order(order_id: int, new_order: OrderBase) -> Order:
  """ Search the given order in the database with its id  """
  for i, order in enumerate(all_orders):
    if order.id == order_id:
      # add the id in the URL to the given order
      new_order_with_id = Order.add_id(new_order, order_id)
      all_orders[i] = new_order_with_id
      return new_order_with_id
  raise HTTPException(status_code=404,
                      detail="Commande introuvable")


@app.delete("/admin/orders/{order_id}",
            description="Supprimer une commande",
            response_description="Commande supprimée",
            status_code=204,
            responses={404: {"model": ErrorMessage,
                             "description": "Commande introuvable"}},
            )
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
