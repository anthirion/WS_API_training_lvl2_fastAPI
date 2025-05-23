# imports for API operation
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, exc, func
from typing import List
from fastapi_pagination import add_pagination
import fastapi_pagination.ext.sqlalchemy as fp_sqlalchemy
from fastapi_pagination.limit_offset import LimitOffsetParams, LimitOffsetPage

from . import models, schemas
from .schemas import ErrorMessage
from .db import engine
from .pagination import DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET


"""
Start the api server
"""
app = FastAPI()
add_pagination(app)

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
                           max_price: float = 99_999_999,
                           limit: int = DEFAULT_PAGINATION_LIMIT,
                           offset: int = DEFAULT_PAGINATION_OFFSET,
                           ) -> LimitOffsetPage[schemas.Product]:
  pagination_params = LimitOffsetParams(limit=limit, offset=offset)
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

      return fp_sqlalchemy.paginate(session,
                                    query=query,
                                    params=pagination_params,
                                    )
    except exc.NoResultFound:
      # no product found in the db
      return LimitOffsetPage[schemas.Product](items=[])


@app.get("/products/{product_id}",
         description="Retourne un objet JSON contenant les détails d'un produit spécifique",
         response_description="	Détails du produit",
         responses={404: {"model": ErrorMessage,
                          "description": "Produit introuvable"}},
         )
async def get_product_by_id(product_id: int) -> schemas.Product:
  with Session(engine) as session:
    try:
      """ Search the product in the database with its id  """
      query = (
          select(models.Product)
          .where(models.Product.id == product_id)
      )
      product = session.execute(query).scalar_one()
    # manage error in case no product was found
    except exc.NoResultFound:
      raise HTTPException(status_code=404,
                          detail="Produit introuvable")
  return product


@app.post("/products",
          description="Ajouter un nouveau produit",
          # status code async defines the status code to return when no error occured
          # since this operation is a creation, return 201 instead of 200
          status_code=201,
          response_description="Produit ajouté",
          responses={409: {"model": ErrorMessage,
                           "description": "Produit déjà existant"}},
          )
async def add_product(new_product: schemas.ProductBase) -> schemas.Product:
  with Session(engine) as session:
    try:
      """
      Check that the product is not already in the database
      """
      query = (
          select(models.Product)
          .where(models.Product.product_name == new_product.product_name,
                 models.Product.description == new_product.description,
                 models.Product.price == new_product.price,
                 models.Product.category == new_product.category,
                 models.Product.stock == new_product.stock,
                 )
      )
      # WARNING: KEEP the .scalar_one() to raise the exception
      session.execute(query).scalar_one()
      raise HTTPException(status_code=409,
                          detail="Produit déjà existant")
    except exc.NoResultFound:
      """ Add the product to the database  """
      # create a product model compatible with SQLAlchemy using the models module
      max_id_query = select(func.max(models.Product.id))
      max_id = session.execute(max_id_query).scalar_one()
      db_product = models.Product(id=max_id + 1,
                                  product_name=new_product.product_name,
                                  description=new_product.description,
                                  price=new_product.price,
                                  category=new_product.category,
                                  stock=new_product.stock,
                                  )
      session.add(db_product)
      # commit to register in the database
      session.commit()
      """ Retrieve the product and its id in the database  """
      query = (
          select(models.Product)
          .where(models.Product.product_name == new_product.product_name,
                 models.Product.description == new_product.description,
                 models.Product.price == new_product.price,
                 models.Product.category == new_product.category,
                 models.Product.stock == new_product.stock,
                 )
      )
      return session.execute(query).scalar_one()


@app.put("/products/{product_id}",
         description="Modifier un produit existant",
         response_description="Produit mis à jour",
         responses={404: {"model": ErrorMessage,
                          "description": "Produit introuvable"}},
         )
async def modify_product(product_id: int, new_product: schemas.ProductBase) -> schemas.Product:
  with Session(engine) as session:
    """ Search the given product in the database with its name  """
    query = (
        update(models.Product)
        .where(models.Product.id == product_id)
        .values(product_name=new_product.product_name,
                description=new_product.description,
                price=new_product.price,
                category=new_product.category,
                stock=new_product.stock,
                )
    )
    rows_affected = session.execute(query).rowcount
    if rows_affected == 0:
      # no row was changed
      raise HTTPException(status_code=404,
                          detail="Produit introuvable")
    # Do not forget to save changes in the database
    session.commit()
    """ Retrieve the product and its id in the database  """
    query = (
        select(models.Product)
        .where(models.Product.product_name == new_product.product_name,
               models.Product.description == new_product.description,
               models.Product.price == new_product.price,
               models.Product.category == new_product.category,
               models.Product.stock == new_product.stock,
               )
    )
    return session.execute(query).scalar_one()


@app.delete("/products/{product_id}",
            description="Supprimer un produit",
            status_code=204,
            response_description="Produit supprimé",
            responses={404: {"model": ErrorMessage,
                             "description": "Produit introuvable"}},
            )
async def delete_product(product_id: int):
  with Session(engine) as session:
    """ Search the given product in the database with its name  """
    query = (
        delete(models.Product)
        .where(models.Product.id == product_id)
    )
    rows_affected = session.execute(query).rowcount
    if rows_affected == 0:
      # no row was changed
      raise HTTPException(status_code=404,
                          detail="Produit introuvable")

    # Do not forget to save changes in the database
    session.commit()


"""
Define all endpoints relative to users below
"""


@app.get("/admin/users",
         description="Retourne un tableau JSON contenant les utilisateurs avec leurs détails",
         response_description="	Liste des utilisateurs",
         )
async def get_all_users(username: str = "",
                        email: str = "",
                        limit: int = DEFAULT_PAGINATION_LIMIT,
                        offset: int = DEFAULT_PAGINATION_OFFSET,
                        ) -> LimitOffsetPage[schemas.User]:
  pagination_params = LimitOffsetParams(limit=limit, offset=offset)
  with Session(engine) as session:
    try:
      query = select(models.User)
      if username:
        """ Retrieve all elements of name "name" if the name parameter is declared  """
        query = query.where(models.User.username == username)
      elif email:
        """ Retrieve all elements of email "email" if the email parameter is declared  """
        query = query.where(models.User.email == email)

      return fp_sqlalchemy.paginate(session,
                                    query=query,
                                    params=pagination_params,
                                    )
    # manage error in case no user was found
    except exc.NoResultFound:
      return LimitOffsetPage[schemas.Product](items=[])


@app.get("/admin/users/{user_id}",
         description="Retourne un objet JSON contenant les détails d'un utilisateur spécifique",
         response_description="	Détails du utilisateur",
         responses={404: {"model": ErrorMessage,
                          "description": "Utilisateur introuvable"}},
         )
async def get_user_by_id(user_id: int) -> schemas.User:
  with Session(engine) as session:
    try:
      """ Search the user in the database with its id  """
      query = (
          select(models.User)
          .where(models.User.id == user_id)
      )
      user = session.execute(query).scalar_one()
    # manage error in case no user was found
    except exc.NoResultFound:
      raise HTTPException(status_code=404,
                          detail="Utilisateur introuvable")
  return user


@app.post("/users",
          description="Ajouter un nouveau utilisateur",
          # status code async defines the status code to return when no error occured
          # since this operation is a creation, return 201 instead of 200
          status_code=201,
          response_description="Utilisateur ajouté",
          responses={409: {"model": ErrorMessage,
                           "description": "Utilisateur déjà existant"}},
          )
async def add_user(new_user: schemas.UserBase) -> schemas.User:
  with Session(engine) as session:
    try:
      """
      Check that the user is not already in the database
      2 users are considered identical if they have the same name
      """
      query = (
          select(models.User)
          .where(models.User.username == new_user.username,
                 models.User.email == new_user.email,
                 models.User.address == new_user.address,
                 models.User.password == new_user.password,
                 )
      )
      # WARNING: KEEP the .scalar_one() to raise the exception
      session.execute(query).scalar_one()
      raise HTTPException(status_code=409,
                          detail="Utilisateur déjà existant")
    except exc.NoResultFound:
      """ Add the user to the database  """
      # create a user model compatible with SQLAlchemy using the models module
      max_id_query = select(func.max(models.User.id))
      max_id = session.execute(max_id_query).scalar_one()
      db_user = models.User(id=max_id + 1,
                            username=new_user.username,
                            email=new_user.email,
                            address=new_user.address,
                            password=new_user.password,
                            )
      session.add(db_user)
      # commit to register in the database
      session.commit()
      """ Retrieve the user and its id in the database  """
      query = (
          select(models.User)
          .where(models.User.username == new_user.username,
                 models.User.email == new_user.email,
                 models.User.address == new_user.address,
                 models.User.password == new_user.password,
                 )
      )
      return session.execute(query).scalar_one()


@app.put("/admin/users/{user_id}",
         description="Modifier un utilisateur existant",
         response_description="Utilisateur mis à jour",
         responses={404: {"model": ErrorMessage,
                          "description": "Utilisateur introuvable"}},
         )
async def modify_user(user_id: int, new_user: schemas.UserBase) -> schemas.User:
  with Session(engine) as session:
    """ Search the given user in the database with its id  """
    query = (
        update(models.User)
        .where(models.User.id == user_id)
        .values(username=new_user.username,
                email=new_user.email,
                address=new_user.address,
                password=new_user.password,
                )
    )
    rows_affected = session.execute(query).rowcount
    if rows_affected == 0:
      raise HTTPException(status_code=404,
                          detail="Utilisateur introuvable")

    # Do not forget to save changes in the database
    session.commit()
    """ Retrieve the user and its id in the database  """
    query = (
        select(models.User)
        .where(models.User.username == new_user.username,
               models.User.email == new_user.email,
               models.User.address == new_user.address,
               models.User.password == new_user.password,
               )
    )
    return session.execute(query).scalar_one()


@app.delete("/admin/users/{user_id}",
            description="Supprimer un utilisateur",
            status_code=204,
            response_description="Utilisateur supprimé",
            responses={404: {"model": ErrorMessage,
                             "description": "Utilisateur introuvable"}},
            )
async def delete_user(user_id: int):
  with Session(engine) as session:
    """ Search the given user in the database with its name  """
    query = (
        delete(models.User)
        .where(models.User.id == user_id)
    )
    rows_affected = session.execute(query).rowcount
    if rows_affected == 0:
      # no row was changed
      raise HTTPException(status_code=404,
                          detail="Utilisateur introuvable")

    # Do not forget to save changes in the database
    session.commit()


"""
Define all endpoints relative to orders below
"""


@app.get("/admin/orders",
         description="Retourne un tableau JSON contenant les commandes avec leurs détails",
         response_description="Liste des commandes",
         )
async def get_all_orders(total: float = 0.0,
                         status: str = "",
                         limit: int = DEFAULT_PAGINATION_LIMIT,
                         offset: int = DEFAULT_PAGINATION_OFFSET,
                         ) -> LimitOffsetPage[schemas.Order]:
  pagination_params = LimitOffsetParams(limit=limit, offset=offset)
  with Session(engine) as session:
    try:
      query = select(models.Order)
      if total < 0:
        raise HTTPException(
            status_code=400,
            detail="Total parameter must be positive"
        )
      if total > 0:
        query = query.where(models.Order.total == total)
      if status:
        query = query.where(models.Order.status == status)

      return fp_sqlalchemy.paginate(session,
                                    query=query,
                                    params=pagination_params,
                                    )
    except exc.NoResultFound:
      return LimitOffsetPage[schemas.Order](items=[])


@app.get("/admin/orders/{order_id}",
         description="Retourne un objet JSON contenant les détails d'une commande spécifique",
         response_description="	Détails de la commande",
         responses={404: {"model": ErrorMessage,
                          "description": "Commande introuvable"}},
         )
async def get_order_by_id(order_id: int) -> schemas.Order:
  with Session(engine) as session:
    try:
      """ Search the order in the database with its id  """
      query = (
          select(models.Order)
          .where(models.Order.id == order_id)
      )
      order = session.execute(query).scalar_one().to_dict()
    # manage error in case no order was found
    except exc.NoResultFound:
      raise HTTPException(status_code=404,
                          detail="Commande introuvable")
  return order


@app.post("/admin/orders",
          description="Ajouter une nouvelle commande",
          response_description="Commande ajoutée",
          status_code=201,
          responses={409: {"model": ErrorMessage,
                           "description": "Commande déjà existante"},
                      400: {"model": ErrorMessage,
                            "description": "Commande incorrecte"}},
          )
async def add_order(new_order: schemas.OrderBase) -> schemas.Order:
  with Session(engine) as session:
    try:
      """
      Check that the order is not already in the database
      2 orders are considered identical if they have the same user, total and status
      """
      query = (
          select(models.Order)
          .where(models.Order.user_id == new_order.user_id,
                 models.Order.total == new_order.total,
                 models.Order.status == new_order.status,
                 )
      )
      # WARNING: KEEP the .scalar_one() to raise the exception
      session.execute(query).scalar_one()
      raise HTTPException(status_code=409,
                          detail="Commande déjà existante")
    except exc.NoResultFound:
      """ The order is not in the db  """
      try:
        assert new_order.amount_is_correct()
        assert new_order.status in schemas.allowed_status
        for item in new_order.items:
          assert item.ordered_quantity > 0
          """ Update the stock of the product in the products table """
          # update the stock of the ordered product
          query = (
              select(models.Product)
              .where(models.Product.id == item.product_id)
          )
          product = session.execute(query).scalar_one()
          new_stock = product.stock - item.ordered_quantity
          assert new_stock >= 0
          # update the product's stock
          query = (
              update(models.Product)
              .where(models.Product.id == item.product_id)
              .values(stock=new_stock)
          )
          session.execute(query)
          session.commit()

        """  Add a new row in the orders table   """
        max_id_query = select(func.max(models.Order.id))
        max_id = session.execute(max_id_query).scalar_one()
        query = (
            insert(models.Order)
            .values(id=max_id + 1,
                    user_id=new_order.user_id,
                    total=new_order.total,
                    status=new_order.status,
                    )
        )
        session.execute(query)
        session.commit()
        """ Retrieve the order and its id in the database  """
        query = (
            select(models.Order)
            .where(models.Order.user_id == new_order.user_id,
                   #    models.Order.total == new_order.total,
                   models.Order.status == new_order.status,
                   )
        )
        db_order = session.execute(query).scalar_one()
        """  Add rows corresponding to the items in the orderlines table   """
        # WARNING: the update of the orderlines table should be made AFTER
        # the update of the orders table to respect DB integrity
        for item in new_order.items:
          max_id_query = select(func.max(models.OrderLine.id))
          max_id = session.execute(max_id_query).scalar_one()
          query = (
              insert(models.OrderLine)
              .values(id=max_id + 1,
                      product_id=item.product_id,
                      ordered_quantity=item.ordered_quantity,
                      order_id=db_order.id,
                      unit_price=item.unit_price,
                      )
          )
          session.execute(query)
          session.commit()
        return db_order.to_dict()
      except (AssertionError):
        raise HTTPException(status_code=400,
                            detail="Commande incorrecte")


@app.put("/admin/orders/{order_id}",
         description="Modifier une commande existante",
         response_description="Commande mise à jour",
         responses={404: {"model": ErrorMessage,
                          "description": "Commande introuvable"},
                     400: {"model": ErrorMessage,
                           "description": "Commande incorrecte"}},
         )
async def modify_order(order_id: int, new_order: schemas.OrderBase) -> schemas.Order:
  with Session(engine) as session:
    try:
      # check that the provided order is correct
      assert new_order.amount_is_correct()
      assert new_order.status in schemas.allowed_status
      """ Search the given order in the database with its id  """
      query = (
          update(models.Order)
          .where(models.Order.id == order_id)
          .values(user_id=new_order.user_id,
                  total=new_order.total,
                  status=new_order.status,
                  )
      )
      rows_affected = session.execute(query).rowcount
      if rows_affected == 0:
        raise HTTPException(status_code=404,
                            detail="Commande introuvable")
      # Do not forget to save changes in the database
      session.commit()
      """
            Modify the orderlines table with the provided items
            Strategy (not the best): delete all orderlines concerning this order
            and add rows corresponding to the items
            """
      query = (
          delete(models.OrderLine)
          .where(models.OrderLine.order_id == order_id)
      )
      session.execute(query)
      session.commit()

      for item in new_order.items:
        max_id_query = select(func.max(models.OrderLine.id))
        max_id = session.execute(max_id_query).scalar_one()
        query = (
            insert(models.OrderLine)
            .values(id=max_id + 1,
                    product_id=item.product_id,
                    ordered_quantity=item.ordered_quantity,
                    order_id=order_id,
                    unit_price=item.unit_price,
                    )
        )
        session.execute(query)
        session.commit()
      """ Retrieve the order and its id in the database  """
      query = (
          select(models.Order)
          .where(models.Order.user_id == new_order.user_id,
                 #    models.Order.total == new_order.total,
                 models.Order.status == new_order.status,
                 )
      )
      db_order = session.execute(query).scalar_one()
      return db_order.to_dict()
    except (AssertionError, exc.NoResultFound):
      raise HTTPException(status_code=400,
                          detail="Commande incorrecte")


@app.delete("/admin/orders/{order_id}",
            description="Supprimer une commande",
            response_description="Commande supprimée",
            status_code=204,
            responses={404: {"model": ErrorMessage,
                             "description": "Commande introuvable"}},
            )
async def delete_order(order_id: int):
  with Session(engine) as session:
    try:
      """ Check that the order to delete exists """
      query = (
          select(models.OrderLine)
          .where(models.OrderLine.order_id == order_id)
      )
      session.execute(query)
    except exc.NoResultFound:
      raise HTTPException(status_code=404,
                          detail="Commande introuvable")
    else:
      """ Delete lines corresponding to the order to delete in the orderlines table """
      # WARNING: the update of the orderlines table should be made BEFORE
      # the update of the orders table to respect DB integrity
      query = (
          delete(models.OrderLine)
          .where(models.OrderLine.order_id == order_id)
      )
      session.execute(query)
      session.commit()

      """ Delete lines corresponding to the order to delete in the orders table """
      query = (
          delete(models.Order)
          .where(models.Order.id == order_id)
      )
      session.execute(query)
      session.commit()
