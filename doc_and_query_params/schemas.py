"""
This module defines a schema used by Pydantic for type checking
"""

from pydantic import BaseModel


class Product(BaseModel):
    """
    This class defines the attributes of Product and their type
    """
    id: int
    name: str
    description: str
    price: float
    category: str
    stock: int


class ErrorMessage(BaseModel):
    """
    Defines a model for API responses in case of an error
    """
    message: str
