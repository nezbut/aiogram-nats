from typing import Any

from aiogram.types import User


async def get_user(event_from_user: User, **_: Any) -> dict[str, Any]:
    """
    Get user information from the given event.

    :param event_from_user: The user object from the event.
    :type event_from_user: User
    :return: A dictionary with user info.
    :rtype: dict[str, Any]
    """
    return {
        "username": event_from_user.first_name,
    }
