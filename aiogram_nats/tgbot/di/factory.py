from dishka import AsyncContainer, Provider, make_async_container

from aiogram_nats.common.settings import Settings
from aiogram_nats.infrastructure.di.broker import get_broker_providers
from aiogram_nats.infrastructure.di.clients import get_clients_providers
from aiogram_nats.infrastructure.di.database import get_database_providers
from aiogram_nats.infrastructure.di.interactors import get_interactors_providers
from aiogram_nats.infrastructure.di.settings import get_settings_providers
from aiogram_nats.infrastructure.di.taskiq_provider import get_taskiq_providers
from aiogram_nats.tgbot.di.bot import get_bot_providers


def get_providers() -> list[Provider]:
    """Returns a list of providers for the main infrastructure components."""
    return [
        *get_settings_providers(),
        *get_database_providers(),
        *get_taskiq_providers(),
        *get_interactors_providers(),
        *get_bot_providers(),
        *get_clients_providers(),
        *get_broker_providers(),
    ]


def create_container(settings: Settings) -> AsyncContainer:
    """Creates an asynchronous container instance."""
    return make_async_container(*get_providers(), context={Settings: settings})
