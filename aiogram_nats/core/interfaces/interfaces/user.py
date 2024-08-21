from collections.abc import Sequence
from typing import Optional, Protocol

from aiogram_nats.core.entities.user import User


class UserUpserter(Protocol):

    """A protocol for upserting users."""

    async def upsert_user(self, user: User) -> User:
        """
        Upserts a user in the system.

        Args :
            user (User): The user to upsert.

        Returns :
            User
        """
        raise NotImplementedError


class UserGetter(Protocol):

    """A protocol for getting users."""

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.

        Args :
            user_id (int): The ID of the user to retrieve.

        Returns :
            Optional[User]: The retrieved User object, or None if no user is found.
        """
        raise NotImplementedError

    async def get_all(self) -> Sequence[User]:
        """
        Retrieves a sequence of all users.

        Returns :
            Sequence[User]: A sequence of retrieved User objects.
        """
        raise NotImplementedError
