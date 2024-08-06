"""
This module defines a schema used by Pydantic for type checking
"""

from pydantic import BaseModel


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


class ErrorMessage(BaseModel):
    """
    Defines a model for API responses in case of an error
    """
    message: str
