"""
This module defines a schema used by Pydantic for type checking
"""

from pydantic import BaseModel
from typing import List

allowed_status = ["Completed", "Pending", "Shipped", "Cancelled"]


class ProductBase(BaseModel):
  """
  A base class defining base product attributes. It defines all attributes except id.
  This class is used for operations that do not need id (the product provided in the body
  of a PUT operation do not have id)
  """
  product_name: str = ""
  description: str = ""
  price: float = 0.0
  category: str = ""
  stock: int = 0


class Product(ProductBase):
  """
  This class adds the id attribute to the ProductBase class. It is useful for all operations
  excluding PUT.
  """
  id: int

  @staticmethod
  def add_id(product_base: ProductBase, id_: int):
    """
    Adds an id to the given product base
    """
    # model_dump generates a dictionary representation of the model
    return Product(id=id_, **product_base.model_dump())


class UserBase(BaseModel):
  """
  A base class defining base user attributes. It defines all attributes except id.
  This class is used for operations that do not need id (the product provided in the body
  of a PUT operation do not have id)
  """
  username: str
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
  def add_id(user_base: UserBase, id_: int):
    """
    Adds an id to the given user base
    """
    # model_dump generates a dictionary representation of the model
    return User(id=id_, **user_base.model_dump())


class Item(BaseModel):
  """
  This class represents an ordered product in an order. It has all the attributes of a product,
  plus an ordered quantity
  """
  product_id: int
  ordered_quantity: int
  unit_price: float


class OrderBase(BaseModel):
  """
  A base class defining base order attributes. It defines all attributes except id.
  This class is used for operations that do not need id (the product provided in the body
  of a PUT operation do not have id)
  """
  user_id: int
  items: List[Item]
  total: float
  status: str

  def is_correct(self, products: List[Product]) -> bool:
    """
    Check that the order is correct, that is:
    - the user_id exists in the list of users
    - the products in the order exists (the id is correct)
    - the stock of the product is bigger than the ordered quantity
    - the total amount of the order is correct (equals to the price
    of the products multiplied by the quantity)
    - the status type is allowed (is in the allowed_status list)
    """
    try:
      order_amount = 0
      for item in self.items:
        # check that the products in the order exist
        # Note: the name, description, etc are not checked
        assert item.product_id in {product.id for product in products}
        # check that the products in the order are available
        product = products[item.product_id]
        assert item.ordered_quantity <= product.stock
        # update the product's stock
        product.stock -= item.ordered_quantity
        order_amount += item.unit_price * item.ordered_quantity
      # check that the total amount of the order is correct
      assert round(order_amount, 2) == self.total
      # check that the status is correct
      assert self.status in allowed_status
      return True
    except AssertionError:
      return False


class Order(OrderBase):
  """
  This class adds the id attribute to the OrderBase class. It is useful for all operations
  excluding PUT.
  """
  id: int

  @staticmethod
  def add_id(order_base: OrderBase, id_: int):
    """
    Adds an id to the given order base
    """
    # model_dump generates a dictionary representation of the model
    return Order(id=id_, **order_base.model_dump())
