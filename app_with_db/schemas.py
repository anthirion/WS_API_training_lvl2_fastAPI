"""
This module defines a schema used by Pydantic for type checking
"""

from pydantic import BaseModel
from typing import List
from .db import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models

allowed_status = ["Completed", "Pending", "Shipped", "Cancelled"]


class ProductBase(BaseModel):
  """
  A base class defining base product attributes. It defines all attributes except id.
  This class is used for operations that do not need id (the product provided in the body
  of a PUT operation do not have id)
  """
  # TODO
  pass


class Product(ProductBase):
  """
  This class adds the id attribute to the ProductBase class. It is useful for all operations
  excluding PUT.
  """
  # TODO
  pass


class UserBase(BaseModel):
  """
  A base class defining base user attributes. It defines all attributes except id.
  This class is used for operations that do not need id (the product provided in the body
  of a PUT operation do not have id)
  """
  # TODO
  pass


class User(UserBase):
  """
  This class adds the id attribute to the UserBase class. It is useful for all operations
  excluding PUT.
  """
  # TODO
  pass


class OrderLineBase(BaseModel):
  # TODO
  pass

  def to_dict(self):
    return {
        "product_id": self.product_id,
        "ordered_quantity": self.ordered_quantity,
        "unit_price": self.unit_price,
    }


class OrderLine(OrderLineBase):
  # TODO
  pass

  def to_dict(self):
    return {
        "id": self.id,
        "product_id": self.product_id,
        "ordered_quantity": self.ordered_quantity,
        "unit_price": self.unit_price,
        "order_id": self.order_id
    }


class OrderBase(BaseModel):
  """
  A base class defining base order attributes. It defines all attributes except id.
  This class is used for operations that do not need id (the product provided in the body
  of a PUT operation do not have id)
  """
  # TODO
  pass

  def amount_is_correct(self) -> bool:
    """
    Check that the total attribute is equal to the sum of the prices of
    the ordered products
    """
    amount = 0.0
    """ Retrieve the price of each product of the items list """
    for item in self.items:
      price = 0.0
      with Session(engine) as session:
        query = (
            select(models.Product)
            .where(models.Product.id == item.product_id)
        )
        # we consider that the execution of the query cannot fail
        # because our database contains correct product ids
        product = session.execute(query).scalar_one()
        price = product.price * item.ordered_quantity
        amount += price
    # WARNING: make sure you round up the amount to avoid approximation errors
    return round(amount, 2) == self.total


class Order(OrderBase):
  """
  This class adds the id attribute to the OrderBase class. It is useful for all operations
  excluding PUT.
  """
  # TODO
  pass

  def to_dict(self):
    return {
        "id": self.id,
        "user_id": self.user_id,
        "items": self.items,
        "total": self.total,
        "status": self.status
    }


"""
Error messages model
"""


class ErrorMessage(BaseModel):
  """
  Defines a model for API responses in case of an error
  """
  message: str
