"""
This module defines the model used by SQLAlchemy for Product
in order to map the object to the SQL table Products
"""

from sqlalchemy import Float, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

MAX_STRING_LENGTH: int = 255


class Base(DeclarativeBase):
    pass


class Product(Base):
    # the name of the SQL table associated to this class
    __tablename__ = "products"

    # define product attributes
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                              nullable=False)
    description: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                             nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                          nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        """
        Defines how the product will be displayed
        """
        return f"Product(id={self.id}, name='{self.product_name}', " \
            f"description='{self.description}', " \
            f"price='{self.price}', category='{self.category}', "\
            f"stock='{self.stock}')"


class User(Base):
    # the name of the SQL table associated to this class
    __tablename__ = "users"

    # define product attributes
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                           nullable=False)
    email: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                       nullable=False)
    address: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                         nullable=False)
    password: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                          nullable=False)

    def __repr__(self):
        """
        Defines how the product will be displayed
        """
        return f"User(id={self.id}, name='{self.user_name}', email='{self.email}', " \
            f"address='{self.address}', password='{self.password}')"


class Order(Base):
    # the name of the SQL table associated to this class
    __tablename__ = "orders"

    # define product attributes
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    userId: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                        nullable=False)

    items: Mapped[List["OrderLine"]] = relationship(back_populates="order")

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "items": self.items,
            "total": self.total,
            "status": self.status,
        }

    def __repr__(self):
        """
        Defines how the product will be displayed
        """
        return f"Order(id={self.id}, userId='{self.userId}'" \
            f"total={self.total}, status='{self.status}', "\
            f"items='{self.items}')"


class OrderLine(Base):
    # the name of the SQL table associated to this class
    __tablename__ = "orderlines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    productId: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    productQuantity: Mapped[int] = mapped_column(Integer)
    orderId: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))

    order: Mapped["Order"] = relationship(back_populates="items")

    def to_dict(self):
        return {
            "id": self.id,
            "productId": self.productId,
            "productQuantity": self.productQuantity,
            "orderId": self.orderId,
        }

    def __repr__(self):
        """
        Defines how the product will be displayed
        """
        return f"OrderLine(id='{self.id}', " \
            f"productId = {self.productId}, " \
            f"productQuantity = '{self.productQuantity}', " \
            f"orderId = '{self.orderId}')"
