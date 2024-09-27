from aiogram import Dispatcher

from aiogram_nats.tgbot.handlers.commands import commands_router


def setup(dp: Dispatcher) -> None:
    """Setup all handlers."""
    dp.include_routers(
        commands_router,
    )
