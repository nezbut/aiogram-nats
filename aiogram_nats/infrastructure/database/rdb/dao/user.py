from collections.abc import Sequence

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram_nats.core.entities.user import User as UserEntity
from aiogram_nats.infrastructure.database.mappers.rdb import userdb_to_entity
from aiogram_nats.infrastructure.database.rdb.dao.base import BaseDAO
from aiogram_nats.infrastructure.database.rdb.models import User


class UserDAO(BaseDAO[User]):

    """A class representing the DAO for the User model."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

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

    async def upsert_user(self, user: User) -> UserEntity:
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
        }
        saved_user = await self.session.execute(
            insert(User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(
                    User.id,), set_=kwargs, where=User.id == user.id,
            )
            .returning(User),
        )
        return userdb_to_entity(saved_user.scalar_one())

    async def get_all(self) -> Sequence[UserEntity]:
        """
        Retrieves all User objects from the database.

        Returns :
            Sequence[User]: A sequence of all User objects.
        """
        users = await self._get_all()
        return [userdb_to_entity(user) for user in users]
