from fastapi import FastAPI, HTTPException
from typing import List

from .products import all_products, Product

from pydantic import BaseModel


class ErrorMessage(BaseModel):
    """
    Defines a model for API responses in case of an error
    """
    message: str


# start the API server
app = FastAPI()


@app.get("/")
def welcome():
    return "Welcome to the API training"


@app.get("/products",
         description="Retourne un tableau JSON contenant les produits avec leurs détails",
         # response_description is the description to display when no error occured (code 200)
         response_description="	Liste des produits",
         )
# Declare query parameters for name and category only (makes more sense)
# WARNING: Do NOT add quotes for query parameters -> products?category=Alimentation
def get_all_products(name: str = "", category: str = "") -> List[Product]:
    if name:
        # name parameter is specified by the user
        return [product for product in all_products
                if product.name == name]
    elif category:
        # category parameter is specified by the user
        return [product for product in all_products
                if product.category == category]
    else:
        # no query parameter is specified by the user
        return all_products


@app.get("/products/{product_id}",
         description="Retourne un objet JSON contenant les détails d'un produit spécifique",
         response_description="	Détails du produit",
         # responses enables you to define additional responses code and message
         # the default code responses are 200 and 422
         responses={404: {"model": ErrorMessage}},
         )
def get_product_by_id(product_id: int) -> Product:
    for product in all_products:
        if product.id == product_id:
            return product
    # if no product is found, raise an error
    raise HTTPException(status_code=404, detail="Produit non trouvé")


@app.post("/products",
          description="Ajouter un nouveau produit",
          # status code defines the status code to return when no error occured
          # since this operation is a creation, return 201 instead of 200
          status_code=201,
          response_description="Produit ajouté",
          responses={409: {"model": ErrorMessage}},
          )
def add_product(product: Product) -> Product:
    if product not in all_products:
        all_products.append(product)
        return product
    else:
        raise HTTPException(status_code=409,
                            detail="Produit déjà existant")


@app.put("/products/{product_id}",
         description="Modifier un produit existant",
         response_description="Produit mis à jour",
         responses={404: {"model": ErrorMessage}},
         )
def modify_product(new_product: Product) -> Product:
    for product in all_products:
        if product.id == new_product.id:
            product = new_product
            return product
    raise HTTPException(status_code=404,
                        detail="Produit non trouvé")
