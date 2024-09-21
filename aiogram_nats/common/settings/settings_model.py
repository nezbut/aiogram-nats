from dataclasses import dataclass
from functools import lru_cache
from typing import Any, TypeVar

from adaptix import Retort
from adaptix.load_error import AggregateLoadError, NoRequiredFieldsLoadError

from aiogram_nats.common.settings.dynaconf_config import dynaconf_settings
from aiogram_nats.common.settings.models import get_retort_providers
from aiogram_nats.common.settings.models.broker import BrokerSettings
from aiogram_nats.common.settings.models.db import DBSettings
from aiogram_nats.common.settings.models.logs import LoggingSettings
from aiogram_nats.common.settings.models.mailing_service import MailingServiceSettings
from aiogram_nats.common.settings.models.telegram import TelegramBot

_DataClass = TypeVar("_DataClass")

_settings_retort = Retort(
    recipe=[*get_retort_providers()],
)


@dataclass
class Settings:

    """A class representing the application settings."""

    bot: TelegramBot
    logging: LoggingSettings
    db: DBSettings
    broker: BrokerSettings
    mailing_service: MailingServiceSettings

    @classmethod
    @lru_cache
    def from_dynaconf(cls) -> "Settings":
        """
        A class method that creates a Settings instance from dynaconf settings.

        It loads the settings from dynaconf and returns a Settings instance with the loaded settings.

        Returns :
            Settings: A Settings instance
        """
        bot = cls._get_settings("bot", TelegramBot)
        db = cls._get_settings("db", DBSettings)
        broker = cls._get_settings("broker", BrokerSettings)
        logs = cls._get_settings("logging", LoggingSettings)
        mailing = cls._get_settings("mailing_service", MailingServiceSettings)

        return cls(bot=bot, logging=logs, db=db, broker=broker, mailing_service=mailing)

    @staticmethod
    def _get_settings(key: str, class_: type[_DataClass]) -> _DataClass:
        key_settings: dict[str, Any] = dynaconf_settings.get(key) or {}
        try:
            settings = _settings_retort.load(key_settings, class_)
        except AggregateLoadError as e:
            try:
                exc: NoRequiredFieldsLoadError = next(
                    exception for exception in e.exceptions
                    if isinstance(exception, NoRequiredFieldsLoadError)
                )
                key_settings.update({key_: {} for key_ in exc.fields})
                settings = _settings_retort.load(key_settings, class_)
            except StopIteration:
                raise e from e
        return settings
