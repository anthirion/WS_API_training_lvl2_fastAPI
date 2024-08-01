"""
This module defines the model used by SQLAlchemy for Product
in order to map the object to the SQL table Products
"""

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

STRING_LENGTH: int = 255


class Base(DeclarativeBase):
    pass


class Product(Base):
    # the name of the SQL table associated to this class
    __tablename__ = "products"

    # define product attributes
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(STRING_LENGTH), nullable=False)
    description: Mapped[str] = mapped_column(String(STRING_LENGTH),
                                             nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(
        String(STRING_LENGTH), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        """
        Defines how the product will be displayed
        """
        return f"Product(id={self.id}, name='{self.name}', " \
            f"description='{self.description}', " \
            f"price={self.price}, category='{self.category}', "\
            f"stock={self.stock})"