from typing import Any, Optional, Protocol, TypedDict

from aiogram import Bot, Router, types
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from aiogram_dialog.api.entities import Context, Stack
from aiogram_dialog.api.protocols import BgManagerFactory, DialogManager
from aiogram_dialog.context.storage import StorageProxy
from dishka import AsyncContainer
from fluentogram import TranslatorHub, TranslatorRunner

from aiogram_nats.common.settings import Settings
from aiogram_nats.common.settings.models import broker, db, logs, mailing_service, telegram
from aiogram_nats.core.interactors import mailing, messages
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler
from aiogram_nats.infrastructure.clients.mailing_service import MailingServiceClient
from aiogram_nats.infrastructure.database.rdb.holder import HolderDAO


class I18nGetter(Protocol):

    def __call__(self, key: str, data: dict[str, Any]) -> str:
        raise NotImplementedError


class AiogramMiddlewareData(TypedDict, total=False):

    """A dictionary containing middleware data for Aiogram."""

    event_from_user: types.User
    event_chat: types.Chat
    bot: Bot
    fsm_storage: BaseStorage
    state: FSMContext
    raw_state: Any
    handler: HandlerObject
    event_update: types.Update
    event_router: Router


class DialogMiddlewareData(TypedDict, total=False):

    """A dictionary containing middleware data for aiogram dialog."""

    dialog_manager: DialogManager
    aiogd_storage_proxy: StorageProxy
    aiogd_stack: Stack
    aiogd_context: Context


class SettingsMiddlewareData(TypedDict, total=False):

    """A dictionary containing middleware data for settings."""

    settings: Settings

    broker_settings: broker.BrokerSettings
    nats_settings: broker.NatsSettings
    tasks_nats_settings: broker.TasksNatsSettings

    db_settings: db.DBSettings
    rdb_settings: db.RDBSettings
    redis_settings: db.RedisSettings
    tasks_redis_settings: db.TasksRedisSettings
    schedule_source: db.TasksScheduleSource
    result_backend: db.TasksResultBackend

    logging_settings: logs.LoggingSettings

    mailing_service_settings: mailing_service.MailingServiceSettings

    telegram_settings: telegram.TelegramBot
    bot_api_settings: telegram.BotApiSettings
    fsm_storage_settings: telegram.FSMStorageSettings
    webhook_settings: Optional[telegram.WebHookSettings]


class MiddlewareData(AiogramMiddlewareData, DialogMiddlewareData, SettingsMiddlewareData, total=False):

    """Middleware data for aiogram."""

    dishka_container: AsyncContainer
    holder_dao: HolderDAO
    scheduler: Scheduler
    bg_manager_factory: BgManagerFactory
    mailing_service: MailingServiceClient
    translator_hub: TranslatorHub
    i18n: TranslatorRunner
    i18n_getter: I18nGetter

    start_mailing: mailing.StartMailing
    schedule_mailing: mailing.ScheduleMailing
    remove_mailing: mailing.RemoveMailing
    create_mailing: mailing.CreateMailing

    schedule_send: messages.ScheduleMessageSend
    schedule_deletion: messages.ScheduleMessageDeletion
