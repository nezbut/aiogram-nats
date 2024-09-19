import asyncio
import logging
from functools import partial

from aiogram import Bot, Dispatcher
from dishka import AsyncContainer
from fastapi import FastAPI

from aiogram_nats.api.factory import create_app
from aiogram_nats.common.settings import Settings
from aiogram_nats.common.settings.models.telegram import WebHookSettings
from aiogram_nats.infrastructure.scheduler.taskiq_constants import taskiq_broker
from aiogram_nats.tgbot import handlers, middlewares
from aiogram_nats.tgbot.di.factory import create_container
from aiogram_nats.tgbot.webhook.fastapi.handlers import SimpleRequestHandler
from aiogram_nats.tgbot.webhook.fastapi.setup import setup_application


def setup_all(dp: Dispatcher, settings: Settings) -> Dispatcher:
    """Setup all in dispatcher."""
    # bg_manager_factory = setup_dialogs(dp, bot_config, message_manager)  # noqa: ERA001
    handlers.setup(dp)
    middlewares.setup(
        dp,
        settings,
        # bg_manager_factory=bg_manager_factory,  # noqa: ERA001
    )
    return dp


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


async def start_polling() -> None:
    """Start polling for telegram bot"""
    settings = Settings.from_dynaconf()
    container = create_container(settings)
    bot: Bot = await container.get(Bot)
    dp_not_setup: Dispatcher = await container.get(Dispatcher)
    dp = setup_all(dp_not_setup, settings)

    logging.basicConfig(level=logging.INFO)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await taskiq_broker.startup()
        await dp.start_polling(bot)
    finally:
        await taskiq_broker.shutdown()
        await bot.session.close()
        await dp.stop_polling()


def start_webhook() -> FastAPI:
    """Start webhook for telegram bot"""
    settings = Settings.from_dynaconf()
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
    asyncio.run(start_polling())
