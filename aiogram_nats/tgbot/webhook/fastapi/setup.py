from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from aiogram import Bot, Dispatcher
from dishka import AsyncContainer
from fastapi import APIRouter, FastAPI

from aiogram_nats.common.log.configuration import LoggerName
from aiogram_nats.common.log.installer import LoggersInstaller
from aiogram_nats.common.settings import Settings
from aiogram_nats.tgbot.setup import setup_dispatcher


def setup_application(app: FastAPI, container: AsyncContainer, /, **kwargs: Any) -> None:
    """Setup webhook application."""
    workflow_data = {
        "app": app,
        "container": container,
        **kwargs,
    }

    @asynccontextmanager
    async def lifespan(*a: Any, **kw: Any) -> AsyncIterator[None]:
        settings = await container.get(Settings)
        dp = await container.get(Dispatcher)
        bot = await container.get(Bot)
        installer = await container.get(LoggersInstaller)
        bot_info = await bot.get_me()
        logger = installer.get_logger(
            LoggerName.BOT, bot_name=bot_info.full_name, id=bot_info.id,
        )
        dispatcher = setup_dispatcher(dp, settings, logger)
        await dispatcher.emit_startup(**workflow_data, **dispatcher.workflow_data)
        yield
        await dispatcher.emit_shutdown(**workflow_data, **dispatcher.workflow_data)

    app.include_router(APIRouter(lifespan=lifespan))
