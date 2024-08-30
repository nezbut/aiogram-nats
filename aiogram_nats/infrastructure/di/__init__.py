from dishka import Provider

from aiogram_nats.infrastructure.di.database import get_database_providers
from aiogram_nats.infrastructure.di.interactors import get_interactors_providers
from aiogram_nats.infrastructure.di.settings import get_settings_providers


def get_main_providers() -> list[Provider]:
    return [
        *get_settings_providers(),
        *get_database_providers(),
        *get_interactors_providers(),
    ]


__all__ = ["get_main_providers"]
