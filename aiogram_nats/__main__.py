import asyncio
import logging
from functools import partial
from typing import Optional

import uvicorn
from aiogram import Bot, Dispatcher
from dishka import AsyncContainer
from fastapi import FastAPI

from aiogram_nats.api.factory import create_app
from aiogram_nats.common.settings import Settings
from aiogram_nats.common.settings.models.telegram import WebHookSettings
from aiogram_nats.infrastructure.scheduler.taskiq_constants import taskiq_broker
from aiogram_nats.tgbot.di.factory import create_container
from aiogram_nats.tgbot.setup import setup_dispatcher
from aiogram_nats.tgbot.webhook.fastapi.handlers import SimpleRequestHandler
from aiogram_nats.tgbot.webhook.fastapi.setup import setup_application


async def startup_api(container: AsyncContainer, settings: WebHookSettings) -> None:
    """Startup webhook"""
    url = settings.url + settings.path
    await taskiq_broker.startup()
    bot: Bot = await container.get(Bot)
    await bot.set_webhook(
        url=url,
        secret_token=settings.secret_token.value,
    )


async def shutdown_api(container: AsyncContainer) -> None:
    """Shutdown webhook"""
    bot: Bot = await container.get(Bot)
    await taskiq_broker.shutdown()
    await bot.session.close()


async def start_polling(settings: Settings) -> None:
    """Start polling for telegram bot"""
    container = create_container(settings)
    bot: Bot = await container.get(Bot)
    dp_not_setup: Dispatcher = await container.get(Dispatcher)
    dp = setup_dispatcher(dp_not_setup, settings)

    logging.basicConfig(level=logging.INFO)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await taskiq_broker.startup()
        await dp.start_polling(bot)
    finally:
        await taskiq_broker.shutdown()
        await bot.session.close()
        await dp.stop_polling()


def start_webhook(settings: Optional[Settings] = None) -> FastAPI:
    """Start webhook for telegram bot"""
    settings = settings or Settings.from_dynaconf()
    if not settings.bot.webhook:
        raise OSError("Webhook settings are not provided")
    container = create_container(settings)
    app = create_app(container)
    setup_application(app, container)
    handler = SimpleRequestHandler(
        secret_token=settings.bot.webhook.secret_token.value,
    )
    handler.register(app, path=settings.bot.webhook.path)
    startup = partial(
        startup_api,
        container=container,
        settings=settings.bot.webhook,
    )
    shutdown = partial(shutdown_api, container=container)
    app.router.add_event_handler("startup", startup)
    app.router.add_event_handler("shutdown", shutdown)

    return app


if __name__ == "__main__":
    settings = Settings.from_dynaconf()
    if settings.bot.webhook:
        app = start_webhook(settings)
        uvicorn.run(
            app=app,
            host="localhost",
            port=8080,
        )
    else:
        asyncio.run(start_polling(settings))
