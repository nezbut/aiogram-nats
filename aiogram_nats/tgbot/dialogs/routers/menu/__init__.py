from aiogram_dialog import Dialog

from . import dialogs


def get_menu_dialogs() -> list[Dialog]:
    """
    Returns a list of Dialog objects.

    :return: A list of Dialog objects.
    :rtype: list[Dialog]
    """
    return [
        dialogs.menu_dialog,
    ]
