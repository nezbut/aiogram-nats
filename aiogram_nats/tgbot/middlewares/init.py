from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog.api.protocols import BgManagerFactory

from aiogram_nats.common.settings import Settings
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler
from aiogram_nats.infrastructure.clients.mailing_service import MailingServiceClient
from aiogram_nats.infrastructure.database.rdb.holder import HolderDAO
from aiogram_nats.tgbot.utils.data import MiddlewareData


class InitMiddleware(BaseMiddleware):

    """Init middleware."""

    def __init__(
        self,
        bg_manager_factory: BgManagerFactory,
        settings: Settings,
    ) -> None:
        self.bg_manager_factory = bg_manager_factory
        self.settings = settings

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Init middleware."""
        container = data["dishka_container"]

        data["bg_manager_factory"] = self.bg_manager_factory
        data["settings"] = self.settings

        data["broker_settings"] = self.settings.broker
        data["nats_settings"] = self.settings.broker.nats
        data["tasks_nats_settings"] = self.settings.broker.nats.tasks

        data["db_settings"] = self.settings.db
        data["rdb_settings"] = self.settings.db.rdb
        data["redis_settings"] = self.settings.db.redis
        data["tasks_redis_settings"] = self.settings.db.redis.tasks
        data["schedule_source"] = self.settings.db.redis.tasks.schedule_source
        data["result_backend"] = self.settings.db.redis.tasks.result_backend

        data["logging_settings"] = self.settings.logging

        data["mailing_service_settings"] = self.settings.mailing_service

        data["telegram_settings"] = self.settings.bot
        data["bot_api_settings"] = self.settings.bot.bot_api
        data["fsm_storage_settings"] = self.settings.bot.fsm_storage
        data["webhook_settings"] = self.settings.bot.webhook

        data["holder_dao"] = await container.get(HolderDAO)
        data["scheduler"] = await container.get(Scheduler)
        data["mailing_service"] = await container.get(MailingServiceClient)

        return await handler(event, data)
