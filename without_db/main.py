from fastapi import FastAPI, HTTPException
from typing import List

from .products import all_products, Product

# start the API server
app = FastAPI()


@app.get("/")
def welcome():
    return "Welcome to the API training"


@app.get("/products/")
def get_all_products() -> List[Product]:
    return all_products


@app.get("/products/{product_id}")
def get_product(product_id: int, ) -> Product:
    product_id = int(product_id)
    for product in all_products:
        if product.id == product_id:
            return product
    # if no product is found, raise an error
    raise HTTPException(status_code=404, detail="Product not found")
