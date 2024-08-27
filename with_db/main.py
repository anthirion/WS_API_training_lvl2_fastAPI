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
def welcome():
    return "Welcome to the API training"


@app.get("/products",
         description="Retourne un tableau JSON contenant les produits avec leurs détails",
         response_description="	Liste des produits",
         )
def get_all_products(name: str = "", category: str = "") -> List[schemas.Product]:
    # start a session to make requests to the database
    with Session(engine) as session:
        try:
            if name:
                """ Retrieve all elements of name "name" if the name parameter is declared  """
                query = (
                    select(models.Product)
                    .where(models.Product.name == name)
                )
                return [session.execute(query).scalar_one()]
            elif category:
                """ Retrieve all elements of category "category" if the category parameter is declared  """
                query = (
                    select(models.Product)
                    .where(models.Product.category == category)
                )
                return [session.execute(query).scalar_one()]
            else:
                """ Retrieve all products if no parameter is declared  """
                query = select(models.Product)
                return session.execute(query).scalars().all()
        # manage error in case no product was found
        except exc.NoResultFound:
            raise HTTPException(status_code=404,
                                detail="No product found")


@app.get("/products/{product_id}",
         description="Retourne un objet JSON contenant les détails d'un produit spécifique",
         response_description="	Détails du produit",
         responses={404: {"model": ErrorMessage}},
         )
def get_product_by_id(product_id: int) -> schemas.Product:
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
                                detail=f"No product with id {product_id} found")
    return product


@app.post("/products",
          description="Ajouter un nouveau produit",
          # status code defines the status code to return when no error occured
          # since this operation is a creation, return 201 instead of 200
          status_code=201,
          response_description="Produit ajouté",
          responses={409: {"model": ErrorMessage}},
          )
def add_product(product: schemas.ProductBase) -> schemas.ProductBase:
    with Session(engine) as session:
        try:
            """
            Check that the product is not already in the database
            2 products are considered identical if they have the same name
            """
            query = (
                select(models.Product)
                .where(models.Product.name == product.name)
            )
            # WARNING: KEEP the .scalar_one() to raise the exception
            session.execute(query).scalar_one()
            raise HTTPException(status_code=409,
                                detail="Produit déjà existant")
        except exc.NoResultFound:
            """ Add the product to the database  """
            # create a product model compatible with SQLAlchemy using the models module
            db_product = models.Product(name=product.name,
                                        description=product.description,
                                        price=product.price,
                                        category=product.category,
                                        stock=product.stock,
                                        )
            session.add(db_product)
            # commit to register in the database
            session.commit()
    return product


@app.put("/products/{product_id}",
         description="Modifier un produit existant",
         response_description="Produit mis à jour",
         responses={404: {"model": ErrorMessage}},
         )
def modify_product(product_id: int, new_product: schemas.ProductBase) -> schemas.ProductBase:
    with Session(engine) as session:
        """ Search the given product in the database with its name  """
        query = (
            update(models.Product)
            .where(models.Product.id == product_id)
            .values(name=new_product.name,
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
                                detail="Le produit à mettre à jour n'existe pas")

        # Do not forget to save changes in the database
        session.commit()
        return new_product


@app.delete("/products/{product_id}",
            description="Supprimer un produit",
            status_code=204,
            response_description="Produit supprimé",
            responses={404: {"model": ErrorMessage}},
            )
def delete_product(product_id: int):
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
                                detail="Le produit à supprimer n'existe pas")

        # Do not forget to save changes in the database
        session.commit()


"""
Define all endpoints relative to users below
"""


@app.get("/admin/users",
         description="Retourne un tableau JSON contenant les utilisateurs avec leurs détails",
         response_description="	Liste des utilisateurs",
         )
def get_all_users(name: str = "", email: str = "") -> List[schemas.User]:
    # start a session to make requests to the database
    with Session(engine) as session:
        try:
            if name:
                """ Retrieve all elements of name "name" if the name parameter is declared  """
                query = (
                    select(models.User)
                    .where(models.User.name == name)
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
            raise HTTPException(status_code=404,
                                detail="No user found")


@app.get("/admin/users/{user_id}",
         description="Retourne un objet JSON contenant les détails d'un utilisateur spécifique",
         response_description="	Détails du utilisateur",
         responses={404: {"model": ErrorMessage}},
         )
def get_user_by_id(user_id: int) -> schemas.User:
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
                                detail=f"No user with id {user_id} found")
    return user


@app.post("/users",
          description="Ajouter un nouveau utilisateur",
          # status code defines the status code to return when no error occured
          # since this operation is a creation, return 201 instead of 200
          status_code=201,
          response_description="Utilisateur ajouté",
          responses={409: {"model": ErrorMessage}},
          )
def add_user(user: schemas.UserBase) -> schemas.UserBase:
    with Session(engine) as session:
        try:
            """
            Check that the user is not already in the database
            2 users are considered identical if they have the same name
            """
            query = (
                select(models.User)
                .where(models.User.name == user.name)
            )
            # WARNING: KEEP the .scalar_one() to raise the exception
            session.execute(query).scalar_one()
            raise HTTPException(status_code=409,
                                detail="Utilisateur déjà existant")
        except exc.NoResultFound:
            """ Add the user to the database  """
            # create a user model compatible with SQLAlchemy using the models module
            db_user = models.User(name=user.name,
                                  email=user.email,
                                  address=user.address,
                                  password=user.password,
                                  )
            session.add(db_user)
            # commit to register in the database
            session.commit()
    return user


@app.put("/admin/users/{user_id}",
         description="Modifier un utilisateur existant",
         response_description="Utilisateur mis à jour",
         responses={404: {"model": ErrorMessage}},
         )
def modify_user(user_id: int, new_user: schemas.UserBase) -> schemas.UserBase:
    with Session(engine) as session:
        """ Search the given user in the database with its id  """
        query = (
            update(models.User)
            .where(models.User.id == user_id)
            .values(name=new_user.name,
                    email=new_user.email,
                    address=new_user.address,
                    password=new_user.password,
                    )
        )
        rows_affected = session.execute(query).rowcount
        if rows_affected == 0:
            raise HTTPException(status_code=404,
                                detail="L'utilisateur à mettre à jour n'existe pas")

        # Do not forget to save changes in the database
        session.commit()
        return new_user


@app.delete("/admin/users/{user_id}",
            description="Supprimer un utilisateur",
            status_code=204,
            response_description="Utilisateur supprimé",
            responses={404: {"model": ErrorMessage}},
            )
def delete_user(user_id: int):
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
                                detail="L'utilisateur à supprimer n'existe pas")

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
def get_order_by_id(order_id: int) -> schemas.Order:
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
                                detail=f"No order with id {order_id} found")
    return order


@app.post("/orders",
          description="Ajouter une nouvelle commande",
          response_description="Commande ajoutée",
          status_code=201,
          responses={409: {"model": ErrorMessage,
                           "description": "Commande déjà existante"},
                      400: {"model": ErrorMessage,
                            "description": "Commande incorrecte"}},
          )
def add_order(order: schemas.OrderBase) -> schemas.OrderBase:
    with Session(engine) as session:
        try:
            """
            Check that the order is not already in the database
            2 orders are considered identical if they have the same user, total and status
            """
            query = (
                select(models.Order)
                .where(models.Order.userId == order.userId,
                       models.Order.total == order.total,
                       models.Order.status == order.status)
            )
            # WARNING: KEEP the .scalar_one() to raise the exception
            order = session.execute(query).scalar_one()
            raise HTTPException(status_code=409,
                                detail="Commande déjà existante")
        except exc.NoResultFound:
            """ The order is not in the db  """
            try:
                assert order.amount_is_correct()
                assert order.status in schemas.allowed_status
                for item in order.items:
                    assert item.productQuantity > 0
                    """ Update the stock of the product in the products table """
                    with Session(engine) as session:
                        # update the stock of the ordered product
                        query = (
                            select(models.Product)
                            .where(models.Product.id == item.productId)
                        )
                        product = session.execute(query).scalar_one()
                        new_stock = product.stock - item.productQuantity
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
                with Session(engine) as session:
                    query = (
                        insert(models.Order)
                        .values(userId=order.userId,
                                total=order.total,
                                status=order.status,
                                )
                    )
                    session.execute(query)
                    session.commit()
                """  Add a new row in the orderlines table   """
                # WARNING: the update of the orderlines table should be made AFTER
                # the update of the orders table to respect DB integrity
                with Session(engine) as session:
                    # get the max id in the order table
                    max_id = session.query(
                        func.max(models.Order.id)).scalar()
                    query = (
                        insert(models.OrderLine)
                        .values(productId=item.productId,
                                productQuantity=item.productQuantity,
                                orderId=max_id,
                                )
                    )
                    session.execute(query)
                    session.commit()
            except (AssertionError, exc.NoResultFound):
                raise HTTPException(status_code=400,
                                    detail="Commande incorrecte")
    return order


@ app.put("/admin/orders/{order_id}",
          description="Modifier une commande existante",
          response_description="Commande mise à jour",
          responses={404: {"model": ErrorMessage,
                           "description": "Commande introuvable"},
                     400: {"model": ErrorMessage,
                           "description": "Commande incorrecte"}},
          )
def modify_order(order_id: int, new_order: schemas.OrderBase) -> schemas.OrderBase:
    try:
        # check that the provided order is correct
        assert new_order.amount_is_correct()
        assert new_order.status in schemas.allowed_status
        """ Search the given order in the database with its id  """
        with Session(engine) as session:
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
                                    detail="L'ordre à mettre à jour n'existe pas")
            # Do not forget to save changes in the database
            session.commit()
        """
        Modify the orderlines table with the provided items
        Strategy (not the best): delete all orderlines concerning this order
        and add rows corresponding to the items
        """
        with Session(engine) as session:
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
                            productQuantity=item.productQuantity,
                            orderId=order_id,
                            )
                )
                session.execute(query)
                session.commit()
    except (AssertionError, exc.NoResultFound):
        raise HTTPException(status_code=400,
                            detail="Commande incorrecte")

    return new_order


@ app.delete("/admin/orders/{order_id}",
             description="Supprimer une commande",
             response_description="Commande supprimée",
             status_code=204,
             responses={404: {"model": ErrorMessage,
                              "description": "Commande introuvable"}},
             )
def delete_order(order_id: int):
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
                                detail="L'ordre à supprimer n'existe pas")
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
