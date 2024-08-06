from fastapi import FastAPI, HTTPException
from typing import List

from .resources import all_products
from .schemas import ProductBase, Product, ErrorMessage

# start the API server
app = FastAPI()


@app.get("/")
def welcome():
    return "Welcome to the API training"

# the parameters of the operation decorators are for documentation purpose only


@app.get("/products",
         description="Retourne un tableau JSON contenant les produits avec leurs détails",
         # response_description is the description to display when no error occured (code 200)
         response_description="	Liste des produits",
         )
# Declare query parameters for name and category only (makes more sense)
# WARNING: Do NOT add quotes for query parameters -> products?category=Alimentation
def get_all_products(name: str = "", category: str = "") -> List[Product]:
    if name:
        """ Retrieve all elements of name "name" if the name parameter is declared  """
        return [product for product in all_products
                if product.name == name]
    elif category:
        """ Retrieve all elements of category "category" if the category parameter is declared  """
        return [product for product in all_products
                if product.category == category]
    else:
        """ Retrieve all products if no parameter is declared  """
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
          response_description="Produit ajouté",
          # status code defines the status code to return when no error occured
          # since this operation is a creation, return 201 instead of 200
          status_code=201,
          responses={409: {"model": ErrorMessage}},
          )
def add_product(product: Product) -> Product:
    """ Check that the product is not already in the database   """
    if product not in all_products:
        all_products.append(product)
        return product
    else:
        raise HTTPException(status_code=409,
                            detail="Produit déjà existant")


@app.put("/products",
         description="Modifier un produit existant",
         response_description="Produit mis à jour",
         responses={404: {"model": ErrorMessage}},
         )
def modify_product(product_id: int, new_product: ProductBase) -> Product:
    """ Search the given product in the database with its id  """
    for i, product in enumerate(all_products):
        if product.id == product_id:
            # add the id in the URL to the given product
            new_product_with_id = Product.add_id(new_product, product_id)
            all_products[i] = new_product_with_id
            return new_product_with_id
    raise HTTPException(status_code=404,
                        detail="Produit non trouvé")


@app.delete("/products/{product_id}",
            description="Supprimer un produit",
            response_description="Produit supprimé",
            status_code=204,
            responses={404: {"model": ErrorMessage}},)
def delete_product(product_id: int):
    """ Search the given product in the database with its id  """
    found = False
    for i, product in enumerate(all_products):
        if product.id == product_id:
            del all_products[i]
            found = True
    if not found:
        raise HTTPException(status_code=404,
                            detail="Produit non trouvé")


"""
Define all endpoints relative to user below
"""
