# imports for API operation
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete, exc
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
async def get_all_products(productName: str = "", product_category: str = "") -> List[schemas.Product]:
    # start a session to make requests to the database
    with Session(engine) as session:
        try:
            if productName:
                """ Retrieve all elements of name "name" if the name parameter is declared  """
                query = (
                    select(models.Product)
                    .where(models.Product.productName == productName)
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


@app.get("/products/{productId}",
         description="Retourne un objet JSON contenant les détails d'un produit spécifique",
         response_description="	Détails du produit",
         responses={404: {"model": ErrorMessage,
                          "description": "Produit introuvable"}},
         )
async def get_product_by_id(productId: int) -> schemas.Product:
    with Session(engine) as session:
        try:
            """ Search the product in the database with its id  """
            query = (
                select(models.Product)
                .where(models.Product.id == productId)
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
                .where(models.Product.productName == new_product.productName,
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
            db_product = models.Product(productName=new_product.productName,
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
                .where(models.Product.productName == new_product.productName,
                       models.Product.description == new_product.description,
                       models.Product.price == new_product.price,
                       models.Product.category == new_product.category,
                       models.Product.stock == new_product.stock,
                       )
            )
            return session.execute(query).scalar_one()


@app.put("/products/{productId}",
         description="Modifier un produit existant",
         response_description="Produit mis à jour",
         responses={404: {"model": ErrorMessage,
                          "description": "Produit introuvable"}},
         )
async def modify_product(productId: int, new_product: schemas.ProductBase) -> schemas.Product:
    with Session(engine) as session:
        """ Search the given product in the database with its name  """
        query = (
            update(models.Product)
            .where(models.Product.id == productId)
            .values(productName=new_product.productName,
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
            .where(models.Product.productName == new_product.productName,
                   models.Product.description == new_product.description,
                   models.Product.price == new_product.price,
                   models.Product.category == new_product.category,
                   models.Product.stock == new_product.stock,
                   )
        )
        return session.execute(query).scalar_one()


@app.delete("/products/{productId}",
            description="Supprimer un produit",
            status_code=204,
            response_description="Produit supprimé",
            responses={404: {"model": ErrorMessage,
                             "description": "Produit introuvable"}},
            )
async def delete_product(productId: int):
    with Session(engine) as session:
        """ Search the given product in the database with its name  """
        query = (
            delete(models.Product)
            .where(models.Product.id == productId)
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
async def get_all_users(username: str = "", email: str = "") -> List[schemas.User]:
    # start a session to make requests to the database
    with Session(engine) as session:
        try:
            if username:
                """ Retrieve all elements of name "name" if the name parameter is declared  """
                query = (
                    select(models.User)
                    .where(models.User.username == username)
                )
                return [session.execute(query).scalar_one()]
            elif email:
                """ Retrieve all elements of email "email" if the email parameter is declared  """
                query = (
                    select(models.User)
                    .where(models.User.email == email)
                )
                return [session.execute(query).scalar_one()]
            else:
                """ Retrieve all users if no parameter is declared  """
                query = select(models.User)
                return session.execute(query).scalars().all()
        # manage error in case no user was found
        except exc.NoResultFound:
            return {}


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
            db_user = models.User(username=new_user.username,
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


@ app.get("/admin/orders",
          description="Retourne un tableau JSON contenant les commandes avec leurs détails",
          response_description="Liste des commandes",
          )
async def get_all_orders() -> List[schemas.Order]:
    with Session(engine) as session:
        query = select(models.Order)
        orders = session.execute(query).scalars().all()
        return [order.to_dict() for order in orders]


@ app.get("/admin/orders/{order_id}",
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
                .where(models.Order.userId == new_order.userId,
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
                    assert item.orderedQuantity > 0
                    """ Update the stock of the product in the products table """
                    # update the stock of the ordered product
                    query = (
                        select(models.Product)
                        .where(models.Product.id == item.productId)
                    )
                    product = session.execute(query).scalar_one()
                    new_stock = product.stock - item.orderedQuantity
                    assert new_stock >= 0
                    # update the product's stock
                    query = (
                        update(models.Product)
                        .where(models.Product.id == item.productId)
                        .values(stock=new_stock)
                    )
                    session.execute(query)
                    session.commit()

                """  Add a new row in the orders table   """
                query = (
                    insert(models.Order)
                    .values(userId=new_order.userId,
                            total=new_order.total,
                            status=new_order.status,
                            )
                )
                session.execute(query)
                session.commit()
                """ Retrieve the order and its id in the database  """
                query = (
                    select(models.Order)
                    .where(models.Order.userId == new_order.userId,
                           #    models.Order.total == new_order.total,
                           models.Order.status == new_order.status,
                           )
                )
                db_order = session.execute(query).scalar_one()
                """  Add rows corresponding to the items in the orderlines table   """
                # WARNING: the update of the orderlines table should be made AFTER
                # the update of the orders table to respect DB integrity
                for item in new_order.items:
                    query = (
                        insert(models.OrderLine)
                        .values(productId=item.productId,
                                orderedQuantity=item.orderedQuantity,
                                orderId=db_order.id,
                                unitPrice=item.unitPrice,
                                )
                    )
                    session.execute(query)
                    session.commit()
                return db_order.to_dict()
            except (AssertionError):
                raise HTTPException(status_code=400,
                                    detail="Commande incorrecte")


@ app.put("/admin/orders/{order_id}",
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
                .values(userId=new_order.userId,
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
                .where(models.OrderLine.orderId == order_id)
            )
            session.execute(query)
            session.commit()

            for item in new_order.items:
                query = (
                    insert(models.OrderLine)
                    .values(productId=item.productId,
                            orderedQuantity=item.orderedQuantity,
                            orderId=order_id,
                            unitPrice=item.unitPrice,
                            )
                )
                session.execute(query)
                session.commit()
            """ Retrieve the order and its id in the database  """
            query = (
                select(models.Order)
                .where(models.Order.userId == new_order.userId,
                       #    models.Order.total == new_order.total,
                       models.Order.status == new_order.status,
                       )
            )
            db_order = session.execute(query).scalar_one()
            return db_order.to_dict()
        except (AssertionError, exc.NoResultFound):
            raise HTTPException(status_code=400,
                                detail="Commande incorrecte")


@ app.delete("/admin/orders/{order_id}",
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
                .where(models.OrderLine.orderId == order_id)
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
                .where(models.OrderLine.orderId == order_id)
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