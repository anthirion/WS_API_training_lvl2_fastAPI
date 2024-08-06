from fastapi import FastAPI, HTTPException
from typing import List

from .schemas import (
    Product, ProductBase,
    User, UserBase
)
from .resources import all_products, all_users

# start the API server
app = FastAPI()


@app.get("/")
def welcome():
    return "Welcome to the API training"


"""
Define all endpoints relative to product below
"""


@app.get("/products")
def get_all_products() -> List[Product]:
    return all_products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int) -> Product:
    for product in all_products:
        if product.id == product_id:
            return product
    # if no product is found, raise an error
    raise HTTPException(status_code=404, detail="Produit non trouvé")


@app.post("/products")
def add_product(product: Product) -> Product:
    """ Check that the product is not already in the database   """
    if product not in all_products:
        all_products.append(product)
        return product
    else:
        raise HTTPException(status_code=404,
                            detail="Produit déjà existant")


@app.put("/products/{product_id}")
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


@app.delete("/products/{product_id}")
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
