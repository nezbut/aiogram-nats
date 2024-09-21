from sqlalchemy.orm import DeclarativeBase


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
