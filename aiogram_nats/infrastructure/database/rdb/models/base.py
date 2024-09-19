from typing import Annotated

from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column

id_int = Annotated[int, mapped_column(BigInteger, primary_key=True)]


class Base(DeclarativeBase):

    """Base class for all database models."""

    repr_cols_num = 2
    repr_cols: tuple = ()

    def __repr__(self) -> str:
        """Returns a string representation of the object."""
        cols = [
            f"{col}={getattr(self, col)}" for index, col in enumerate(self.__table__.columns.keys())
            if col in self.repr_cols or index < self.repr_cols_num
        ]

        return f"{self.__class__.__name__}({', '.join(cols)})"
