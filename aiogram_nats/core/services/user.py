from typing import Optional

from aiogram_nats.core.entities.user import User
from aiogram_nats.core.interfaces.interfaces.user import UserGetter, UserUpserter


async def upsert_user(user: User, upserter: UserUpserter) -> User:
    """
    Inserts or updates a user using the provided upserter.

    Args :
        user (User): The user to be inserted or updated.
        upserter (UserUpserter): The upserter to use for the operation.

    Returns :
        User
    """
    return await upserter.upsert_user(user)


async def get_users(getter: UserGetter, ids: Optional[list[int]] = None) -> list[User]:
    """
    Retrieves a sequence of users using the provided getter.

    Args :
        getter (UserGetter): The getter to use for the operation.

    Returns :
        Sequence[User]: A sequence of retrieved users.
    """
    return await getter.get_all(ids=ids)


async def get_user(user_id: int, getter: UserGetter) -> Optional[User]:
    """
    Retrieves a user by their ID using the provided UserGetter.

    Args :
        user_id (int): The ID of the user to retrieve.
        getter (UserGetter): The UserGetter to use for the operation.

    Returns :
        Optional[User]: The retrieved User object, or None if no user is found.
    """
    return await getter.get_by_id(user_id)
