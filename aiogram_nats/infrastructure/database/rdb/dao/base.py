from collections.abc import Sequence
from typing import Generic, TypeVar, Union
from uuid import UUID

from sqlalchemy import ScalarResult, func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from aiogram_nats.infrastructure.database.rdb.models.base import Base

Model_co = TypeVar("Model_co", bound=Base, covariant=True, contravariant=False)


class BaseDAO(Generic[Model_co]):

    """Base DAO class."""

    def __init__(self, model: type[Model_co], session: AsyncSession) -> None:
        self._model = model
        self.session = session

    async def count(self) -> int:
        """Returns the number of rows in the table."""
        res = await self.session.execute(select(func.count()).select_from(self._model))
        return res.scalar_one()

    async def _get_all(self, options: Sequence[ORMOption] = ()) -> Sequence[Model_co]:
        result: ScalarResult[Model_co] = await self.session.scalars(
            select(self._model).options(*options),
        )
        return result.all()

    async def _get_by_id(
            self, id_: Union[int, UUID, str], *, options: Sequence[ORMOption] | None = None, populate_existing: bool = False,
    ) -> Model_co:
        result = await self.session.get(
            self._model, id_, options=options, populate_existing=populate_existing,
        )
        if result is None:
            raise NoResultFound
        return result

    async def _flush(self, *objects: Base) -> None:
        return await self.session.flush(objects)

    def _add(self, obj: Base) -> None:
        return self.session.add(obj)
