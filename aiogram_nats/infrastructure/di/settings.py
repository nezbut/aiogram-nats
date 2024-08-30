from dishka import Provider, Scope, provide

from aiogram_nats.common.settings import Settings
from aiogram_nats.common.settings.models import broker, db, logs
from aiogram_nats.common.settings.models import mailing_service as ms
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

    @provide
    def get_fsm_storage_settings(self, bot_settings: tg.TelegramBot) -> tg.FSMStorageSettings:
        """Get the FSM storage settings from the given bot settings."""
        return bot_settings.fsm_storage


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
    def get_db_settings(self, settings: Settings) -> db.DBSettings:
        """Provides the database settings from the given settings."""
        return settings.db

    @provide
    def get_rdb_settings(self, db_settings: db.DBSettings) -> db.RDBSettings:
        """Provides the relational database settings from the given database settings."""
        return db_settings.rdb

    @provide
    def get_redis_settings(self, db_settings: db.DBSettings) -> db.RedisSettings:
        """Provides the Redis settings from the given database settings."""
        return db_settings.redis

    @provide
    def get_redis_tasks_settings(self, redis_settings: db.RedisSettings) -> db.TasksRedisSettings:
        """Get the Redis tasks settings from the given Redis settings."""
        return redis_settings.tasks


class BrokerSettingsProvider(Provider):

    """Provider for Broker Settings"""

    scope = Scope.APP

    @provide
    def get_broker_settings(self, settings: Settings) -> broker.BrokerSettings:
        """Provide the broker settings from the given settings."""
        return settings.broker

    @provide
    def get_nats_settings(self, broker_settings: broker.BrokerSettings) -> broker.NatsSettings:
        """Provides the NATS settings from the given broker settings."""
        return broker_settings.nats

    @provide
    def get_nats_tasks_settings(self, nats_settings: broker.NatsSettings) -> broker.TasksNatsSettings:
        """Get the NATS tasks settings from the given NATS settings."""
        return nats_settings.tasks


class MailingServiceSettingsProvider(Provider):

    """Provider for Mailing Service Settings."""

    @provide
    def get_mailing_service_settings(self, settings: Settings) -> ms.MailingServiceSettings:
        """Get the mailing service settings from the given settings."""
        return settings.mailing_service


def get_settings_providers() -> list[Provider]:
    """Returns a list of settings providers for di."""
    return [
        SettingsProvider(),
        BotSettingsProvider(),
        LoggingSettingsProvider(),
        DBSettingsProvider(),
        BrokerSettingsProvider(),
        MailingServiceSettingsProvider(),
    ]
