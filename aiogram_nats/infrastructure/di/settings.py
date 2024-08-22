from dishka import Provider, Scope, provide

from aiogram_nats.common.settings import Settings
from aiogram_nats.common.settings.models import logs, rdb
from aiogram_nats.common.settings.models import telegram as tg


class SettingsProvider(Provider):

    """Provider for Settings"""

    scope = Scope.APP

    @provide
    def get_settings(self) -> Settings:
        """Provide the settings by loading them from dynaconf."""
        return Settings.from_dynaconf()


class BotSettingsProvider(Provider):

    """Provider for Bot Settings"""

    scope = Scope.APP

    @provide
    def get_bot_settings(self, settings: Settings) -> tg.TelegramBot:
        """Provides the Telegram bot settings from the given settings."""
        return settings.bot

    @provide
    def get_bot_api_settings(self, bot_settings: tg.TelegramBot) -> tg.BotApiSettings:
        """Provides the Telegram bot API settings from the given bot settings."""
        return bot_settings.bot_api


class LoggingSettingsProvider(Provider):

    """Provider for Logging Settings"""

    scope = Scope.APP

    @provide
    def get_logging_settings(self, settings: Settings) -> logs.LoggingSettings:
        """Provides the logging settings from the given settings."""
        return settings.logging


class DBSettingsProvider(Provider):

    """Provider for DataBase Settings"""

    scope = Scope.APP

    @provide
    def get_db_settings(self, settings: Settings) -> rdb.DBSettings:
        """Provides the database settings from the given settings."""
        return settings.rdb
