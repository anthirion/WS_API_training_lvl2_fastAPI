# imports for API operation
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, exc
from typing import List

# import list of products and ProductBase class
from . import models, schemas
from .schemas import ErrorMessage
from .db import engine


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
