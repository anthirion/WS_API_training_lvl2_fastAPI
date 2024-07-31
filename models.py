"""
This module defines the model used by SQLAlchemy for Product
in order to map the object to the SQL table Products
"""

from sqlalchemy import Float, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

STRING_LENGTH: int = 255


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(STRING_LENGTH), nullable=False)
    description = Column(String(STRING_LENGTH),
                         nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(STRING_LENGTH), nullable=False)
    stock = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', description='{self.description}'," \
            f"price={self.price}, category='{
                self.category}', stock={self.stock})"
