from dataclasses import dataclass
from typing import Any

from adaptix import NameStyle, Retort, name_mapping

from aiogram_nats.common.settings.dynaconf_config import dynaconf_settings
from aiogram_nats.common.settings.models.logs import LoggingSettings
from aiogram_nats.common.settings.models.rdb import DBSettings
from aiogram_nats.common.settings.models.telegram import TelegramBot

_settings_retort = Retort(
    recipe=[
        name_mapping(
            LoggingSettings,
            name_style=NameStyle.UPPER_SNAKE,
        ),
        name_mapping(
            TelegramBot,
            name_style=NameStyle.UPPER_SNAKE,
        ),
        name_mapping(
            DBSettings,
            name_style=NameStyle.UPPER_SNAKE,
        ),
    ],
)


@dataclass
class Settings:

    """A class representing the application settings."""

    bot: TelegramBot
    logging: LoggingSettings
    rdb: DBSettings

    @classmethod
    def from_dynaconf(cls) -> "Settings":
        """
        A class method that creates a Settings instance from dynaconf settings.

        It loads the settings from dynaconf and returns a Settings instance with the loaded settings.

        Returns :
            Settings: A Settings instance
        """
        bot = _settings_retort.load(cls._get_settings("bot"), TelegramBot)
        rdb = _settings_retort.load(cls._get_settings("rdb"), DBSettings)
        logs = _settings_retort.load(
            cls._get_settings("logging"), LoggingSettings,
        )

        return cls(bot=bot, logging=logs, rdb=rdb)

    @staticmethod
    def _get_settings(key: str) -> dict[str, Any]:
        key_settings: dict[str, Any] = dynaconf_settings.get(key) or {}
        return key_settings
