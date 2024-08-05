"""
This module defines a schema used by Pydantic for type checking
"""

from pydantic import BaseModel


class ProductBase(BaseModel):
    """
    A base class defining base product attributes
    This class is used by child classes for CRUD operations (read, create, etc)
    """
    name: str
    description: str
    price: float
    category: str
    stock: int


class Product(ProductBase):
    """
    This class is used for product retrieval
    When retrieving a product from the API, display its id
    """
    id: int


class ErrorMessage(BaseModel):
    """
    Defines a model for API responses in case of an error
    """
    message: str
