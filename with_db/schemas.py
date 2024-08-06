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


class ErrorMessage(BaseModel):
    """
    Defines a model for API responses in case of an error
    """
    message: str
