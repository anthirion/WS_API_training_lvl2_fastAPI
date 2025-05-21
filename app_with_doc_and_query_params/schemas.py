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
  # TODO
  pass

  def __hash__(self):
    return hash((
        self.product_name,
        self.description,
        self.price,
        self.category,
        self.stock
    ))

  def __eq__(self, other):
    if not isinstance(other, ProductBase):
      raise ValueError("Other object is not a product")

    return (self.product_name == other.product_name and
            self.description == other.description and
            self.price == other.price and
            self.category == other.category and
            self.stock == other.stock)


class Product(ProductBase):
  """
  This class adds the id attribute to the ProductBase class. It is useful for all operations
  excluding PUT.
  """
  # TODO
  pass

  @staticmethod
  def add_id(product_base: ProductBase, id_: int):
    """
    Adds an id to the given product base
    """
    # model_dump generates a dictionary representation of the model
    return Product(id=id_, **product_base.model_dump())

  def __eq__(self, other):
    if not isinstance(other, Product):
      raise ValueError("Other object is not a product")
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)


class UserBase(BaseModel):
  """
  A base class defining base user attributes. It defines all attributes except id.
  This class is used for operations that do not need id (the product provided in the body
  of a PUT operation do not have id)
  """
  # TODO
  pass

  def __hash__(self):
    return hash((
        self.username,
        self.email,
        self.address,
        self.password
    ))

  def __eq__(self, other):
    if not isinstance(other, UserBase):
      raise ValueError("Other object is not a user")

    return (
        self.username == other.username and
        self.email == other.email and
        self.address == other.address and
        self.password == other.password
    )


class User(UserBase):
  """
  This class adds the id attribute to the UserBase class. It is useful for all operations
  excluding PUT.
  """
  # TODO
  pass

  @staticmethod
  def add_id(user_base: UserBase, id_: int):
    """
    Adds an id to the given user base
    """
    # model_dump generates a dictionary representation of the model
    return User(id=id_, **user_base.model_dump())

  def __eq__(self, other):
    if not isinstance(other, User):
      raise ValueError("Other object is not a user")
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)


class Item(BaseModel):
  """
  This class represents an ordered product in an order. It has all the attributes of a product,
  plus an ordered quantity
  """
  # TODO
  pass

  def __hash__(self):
    return hash((
        self.product_id,
        self.ordered_quantity,
        self.unit_price
    ))

  def __eq__(self, other):
    if not isinstance(other, Item):
      raise ValueError("Other object is not an Item")

    return (
        self.product_id == other.product_id and
        self.ordered_quantity == other.ordered_quantity and
        self.unit_price == other.unit_price
    )


class OrderBase(BaseModel):
  """
  A base class defining base order attributes. It defines all attributes except id.
  This class is used for operations that do not need id (the product provided in the body
  of a PUT operation do not have id)
  """
  # TODO
  pass

  def is_correct(self, products: List[Product]) -> bool:
    """
    Check that the order is correct, that is:
    - the user_id exists in the list of users
    - the products in the order exist (the id is correct)
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

  def __hash__(self):
    item_hashes = tuple(sorted(hash(item) for item in self.items))
    return hash((
        self.user_id,
        item_hashes,
        self.total,
        self.status
    ))

  def __eq__(self, other):
    if not isinstance(other, OrderBase):
      raise ValueError("Other object is not an OrderBase")

    if len(self.items) != len(other.items):
      return False

    return (
        self.user_id == other.user_id and
        self.items == other.items and
        self.total == other.total and
        self.status == other.status
    )


class Order(OrderBase):
  """
  This class adds the id attribute to the OrderBase class. It is useful for all operations
  excluding PUT.
  """
  # TODO
  pass

  @staticmethod
  def add_id(order_base: OrderBase, id_: int):
    """
    Adds an id to the given order base
    """
    # model_dump generates a dictionary representation of the model
    return Order(id=id_, **order_base.model_dump())

  def __eq__(self, other):
    if not isinstance(other, Order):
      raise ValueError("Other object is not a order")
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)


"""
Error messages model
"""


class ErrorMessage(BaseModel):
  """
  Defines a model for API responses in case of an error
  """
  message: str
