from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.protocols import BgManagerFactory

from aiogram_nats.tgbot.dialogs.routers import get_dialogs


def setup(dp: Dispatcher) -> BgManagerFactory:
    """Setup dialogs"""
    dialogs = get_dialogs()
    dp.include_routers(*dialogs)
    return setup_dialogs(dp)
