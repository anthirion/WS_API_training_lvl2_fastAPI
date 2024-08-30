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
    product_name: str
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
                       product_name=product.product_name,
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
    user_name: str
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
                    user_name=user.user_name,
                    email=user.email,
                    address=user.address,
                    password=user.password,
                    )


class Item(Product):
    """
    This class represents an ordered product in an order. It has all the attributes of a product,
    plus an ordered quantity
    """
    ordered_quantity: int

    @staticmethod
    def add_ordered_quantity(product: Product, ordered_quantity_: int):
        """
        Adds an id to the given order
        """
        return Item(id=product.id,
                    product_name=product.product_name,
                    description=product.description,
                    price=product.price,
                    category=product.category,
                    stock=product.stock,
                    ordered_quantity=ordered_quantity_,
                    )


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

    def is_correct(self, products: List[Product]) -> bool:
        """
        Check that the order is correct, that is:
        - the userId exists in the list of users
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
                assert item.id in {product.id for product in products}
                # check that the products in the order are available
                product = products[item.id]
                assert item.ordered_quantity <= product.stock
                # update the product's stock
                product.stock -= item.ordered_quantity
                order_amount += item.price * item.ordered_quantity
            # check that the total amount of the order is correct
            assert order_amount == self.total
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


"""
Error messages model
"""


class ErrorMessage(BaseModel):
    """
    Defines a model for API responses in case of an error
    """
    message: str
