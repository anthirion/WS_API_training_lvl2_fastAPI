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


class User(Base):
  # the name of the SQL table associated to this class
  __tablename__ = "users"

  # define product attributes
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                        nullable=False)
  email: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                     nullable=False)
  address: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                       nullable=False)
  password: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                        nullable=False)


class Order(Base):
  # the name of the SQL table associated to this class
  __tablename__ = "orders"

  # define product attributes
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  user_id: Mapped[int] = mapped_column(Integer, nullable=False)
  total: Mapped[float] = mapped_column(Float, nullable=False)
  status: Mapped[str] = mapped_column(String(MAX_STRING_LENGTH),
                                      nullable=False)

  items: Mapped[List["OrderLine"]] = relationship(back_populates="order")

  def to_dict(self):
    return {
        "id": self.id,
        "user_id": self.user_id,
        "items": self.items,
        "total": self.total,
        "status": self.status
    }


class OrderLine(Base):
  # the name of the SQL table associated to this class
  __tablename__ = "orderlines"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
  ordered_quantity: Mapped[int] = mapped_column(Integer)
  order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
  unit_price: Mapped[float] = mapped_column(Float)

  order: Mapped["Order"] = relationship(back_populates="items")

  def to_dict(self):
    return {
        "id": self.id,
        "product_id": self.product_id,
        "ordered_quantity": self.ordered_quantity,
        "order_id": self.order_id,
        "unit_price": self.unit_price
    }
