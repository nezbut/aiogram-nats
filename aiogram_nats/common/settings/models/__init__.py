from typing import Any, Final

from adaptix import NameStyle, Provider, name_mapping

from aiogram_nats.common.settings.models import broker, db, logs, mailing_service, telegram

_settings: Final[list[Any]] = [
    *broker.get_broker_settings(),
    *db.get_db_settings(),
    *logs.get_logging_settings(),
    *telegram.get_telegram_settings(),
    *mailing_service.get_mailing_service_settings(),
]


def get_retort_providers() -> list[Provider]:
    """
    Returns a list of Provider objects that represent the settings for different components of the application.

    :return: A list of Provider objects.
    :rtype: list[Provider]
    """
    return [name_mapping(provider, name_style=NameStyle.UPPER_SNAKE) for provider in _settings]


__all__ = [
    "get_retort_providers",
]
