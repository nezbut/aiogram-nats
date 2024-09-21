from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from dishka import AsyncContainer, Provider, Scope, provide
from dishka.integrations.aiogram import setup_dishka
from nats.aio.client import Client
from nats.js import JetStreamContext

from aiogram_nats.common.settings.models.db import RedisSettings
from aiogram_nats.common.settings.models.telegram import FSMStorageSettings, FSMStorageType, TelegramBot
from aiogram_nats.tgbot.utils.nats_fsm.storage import NatsStorage


class BotProvider(Provider):

    """A provider class for Telegram bot instances."""

    scope = Scope.APP

    @provide
    async def get_bot(self, config: TelegramBot) -> Bot:
        """Provides a Telegram bot instance based on the given configuration."""
        return config.create_bot_instance()


class DpProvider(Provider):

    """The provider class for the Telegram bot dispatcher."""

    scope = Scope.APP

    @provide
    async def create_dispatcher(self, storage: BaseStorage, container: AsyncContainer) -> Dispatcher:
        """Creates a Telegram bot dispatcher instance."""
        dp = Dispatcher(storage=storage)
        setup_dishka(container, dp, auto_inject=True)
        return dp

    @provide
    async def create_storage(
        self,
        fsm_settings: FSMStorageSettings,
        redis_settings: RedisSettings,
        nc: Client,
        js: JetStreamContext,
    ) -> BaseStorage:
        """Creates a fsm storage instance."""
        match fsm_settings.storage_type:
            case FSMStorageType.REDIS:
                db = fsm_settings.redis.db
                redis_uri = redis_settings.make_uri(db=db).value
                return RedisStorage.from_url(redis_uri, connection_kwargs=fsm_settings.redis.connection_kwargs)
            case FSMStorageType.NATS:
                storage = NatsStorage(
                    nc=nc,
                    js=js,
                    nats_storage_settings=fsm_settings.nats,
                )
                if fsm_settings.nats.create_nats_kv_buckets:
                    await storage.create_storage()
                return storage
            case _:
                return MemoryStorage()


def get_bot_providers() -> list[Provider]:
    """Returns a list of providers for the Telegram bot."""
    return [
        DpProvider(),
        BotProvider(),
    ]
