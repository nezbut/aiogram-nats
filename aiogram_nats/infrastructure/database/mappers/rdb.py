from adaptix import dump
from adaptix.conversion import get_converter

from aiogram_nats.core.entities.user import User as UserEntity
from aiogram_nats.infrastructure.database.rdb.models.user import UserORM

userdb_to_entity = get_converter(UserORM, UserEntity)


def user_entity_to_db(user: UserEntity) -> UserORM:
    """Converts a UserEntity object to a UserORM object."""
    user_data = dump(user)
    return UserORM(**user_data)


__all__ = [
    "userdb_to_entity",
    "user_entity_to_db",
]
