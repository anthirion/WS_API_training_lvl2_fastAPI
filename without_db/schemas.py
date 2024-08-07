"""
This module defines a schema used by Pydantic for type checking
"""

from pydantic import BaseModel
from typing import List


class ProductBase(BaseModel):
    """
    A base class defining base product attributes. It defines all attributes except id.
    This class is used for operations that do not need id (the product provided in the body
    of a PUT operation do not have id)
    """
    name: str
    description: str
    price: float
    category: str
    stock: int


class Product(ProductBase):
    """
    This class adds the id attribute to the ProductBase class. It is useful for all operations
    excluding PUT.
    """
    id: int

    @staticmethod
    def add_id(product: ProductBase, id_: int):
        """
        Adds an id to the given product
        """
        return Product(id=id_,
                       name=product.name,
                       description=product.description,
                       price=product.price,
                       category=product.category,
                       stock=product.stock,
                       )


class UserBase(BaseModel):
    """
    A base class defining base user attributes. It defines all attributes except id.
    This class is used for operations that do not need id (the product provided in the body
    of a PUT operation do not have id)
    """
    name: str
    email: str
    address: str
    password: str


class User(UserBase):
    """
    This class adds the id attribute to the UserBase class. It is useful for all operations
    excluding PUT.
    """
    id: int

    @staticmethod
    def add_id(user: UserBase, id_: int):
        """
        Adds an id to the given user
        """
        return User(id=id_,
                    name=user.name,
                    email=user.email,
                    address=user.address,
                    password=user.password,
                    )


class Item(BaseModel):
    productId: int
    quantity: int
    UnitPrice: float


class OrderBase(BaseModel):
    """
    A base class defining base order attributes. It defines all attributes except id.
    This class is used for operations that do not need id (the product provided in the body
    of a PUT operation do not have id)
    """
    userId: int
    items: List[Item]
    total: float
    status: str


class Order(OrderBase):
    """
    This class adds the id attribute to the OrderBase class. It is useful for all operations
    excluding PUT.
    """
    id: int

    @staticmethod
    def add_id(order: OrderBase, id_: int):
        """
        Adds an id to the given order
        """
        return Order(id=id_,
                     userId=order.userId,
                     items=order.items,
                     total=order.total,
                     status=order.status,
                     )
