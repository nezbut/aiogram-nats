from aiogram import Dispatcher

from aiogram_nats.common.settings import Settings
from aiogram_nats.tgbot import dialogs, handlers, middlewares


def setup_dispatcher(dp: Dispatcher, settings: Settings) -> Dispatcher:
    """Setup all in dispatcher."""
    handlers.setup(dp)
    bg_manager_factory = dialogs.setup(dp)
    middlewares.setup(
        dp=dp,
        bg_manager_factory=bg_manager_factory,
        settings=settings,
    )
    return dp
