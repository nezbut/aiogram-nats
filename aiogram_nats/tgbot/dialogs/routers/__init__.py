from aiogram_dialog import Dialog

from .menu import get_menu_dialogs


def get_dialogs() -> list[Dialog]:
    """
    Returns a list of Dialog objects.

    :return: A list of Dialog objects.
    :rtype: list[Dialog]
    """
    return [
        *get_menu_dialogs(),
    ]


__all__ = ["get_dialogs"]
