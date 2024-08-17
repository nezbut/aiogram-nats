from dataclasses import dataclass

from adaptix import NameStyle, Retort, name_mapping

from aiogram_nats.common.settings.dynaconf_config import dynaconf_settings
from aiogram_nats.common.settings.models.logs import LoggingSettings
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
    ],
)


@dataclass
class Settings:

    """A class representing the application settings."""

    bot: TelegramBot
    logging: LoggingSettings

    @classmethod
    def from_dynaconf(cls) -> "Settings":
        """
        A class method that creates a Settings instance from dynaconf settings.

        It loads the settings from dynaconf and returns a Settings instance with the loaded settings.

        Returns :
            Settings: A Settings instance
        """
        bot = _settings_retort.load(dynaconf_settings.bot, TelegramBot)
        logs = _settings_retort.load(
            dynaconf_settings.logging, LoggingSettings,
        )

        return cls(bot=bot, logging=logs)
