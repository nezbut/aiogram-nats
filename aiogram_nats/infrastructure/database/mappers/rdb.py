from adaptix.conversion import get_converter

from aiogram_nats.core.entities.user import User as UserEntity
from aiogram_nats.infrastructure.database.rdb.models.user import User

userdb_to_entity = get_converter(User, UserEntity)

__all__ = [
    "userdb_to_entity",
]
