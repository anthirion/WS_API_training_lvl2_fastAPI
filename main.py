# import list of products and Product class
from products import Product
from products import all_products

from typing import List
from fastapi import FastAPI

app = FastAPI()


@app.get("/products/")
def get_all_products() -> List[Product]:
    return all_products


@app.get("/products/{product_id}")
def get_product(product_id: int) -> Product:
    for product in all_products:
        if product.id == product_id:
            return product
