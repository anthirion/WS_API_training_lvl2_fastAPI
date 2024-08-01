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
