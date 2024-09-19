from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_nats.core.entities.user import User as UserEntity
from aiogram_nats.infrastructure.database.mappers.rdb import userdb_to_entity
from aiogram_nats.infrastructure.database.rdb.dao.base import BaseDAO
from aiogram_nats.infrastructure.database.rdb.models import UserORM


class UserDAO(BaseDAO[UserORM]):

    """A class representing the DAO for the User model."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(UserORM, session)

    async def get_by_id(self, id_: int) -> UserEntity:
        """
        Retrieves a user by their ID.

        Args :
            id_ (int): The ID of the user to retrieve.

        Returns :
            User: The retrieved user entity.
        """
        user = await self._get_by_id(id_)
        return userdb_to_entity(user)

    async def upsert_user(self, user: UserEntity) -> UserEntity:
        """
        Inserts or updates a user in the database.

        Args :
            user (User): The user to be inserted or updated.

        Returns :
            User: The inserted or updated user entity.
        """
        kwargs = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "joined_us": user.joined_us,
        }

        saved_user = await self.session.execute(
            insert(self._model)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(
                    self._model.id,), set_=kwargs, where=self._model.id == user.id,
            )
            .returning(self._model),
        )
        return userdb_to_entity(saved_user.scalar_one())

    async def get_all(self, ids: Optional[list[int]] = None) -> list[UserEntity]:
        """Retrieves a list of users from the database."""
        if not ids:
            users = await self._get_all()
        else:
            users = (await self.session.scalars(select(self._model).where(self._model.id.in_(ids)))).all()
        return [userdb_to_entity(user) for user in users]
