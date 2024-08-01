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
def get_product_by_id(product_id: int) -> Product:
    for product in all_products:
        if product.id == product_id:
            return product
    # if no product is found, raise an error
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products")
def add_product(product: Product) -> Product:
    if product not in all_products:
        all_products.append(product)
        return product
    else:
        raise HTTPException(status_code=404,
                            detail="Already existing product")
