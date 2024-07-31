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

    # configure pydantic to use ORM
    # this will make pydantic use object attributs in addition to dict values
    # class Config:
    #     orm_mode = True


class ProductCreate(ProductBase):
    """
    This class is used for product creation
    When creating a product, you do not know its id
    Therefore, id attribute is absent from this class
    """
    pass
