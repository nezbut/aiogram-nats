from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.session.base import BaseSession
from aiogram.client.telegram import TelegramAPIServer
from nats.js.api import KeyValueConfig

from aiogram_nats.common.settings.models.security import SecretStr


class BotApiType(Enum):

    """
    An enumeration of bot API types.

    Attributes :
        LOCAL (str): The local bot API type.
        OFFICIAL (str): The official bot API type.
    """

    LOCAL = "local"
    OFFICIAL = "official"


class FSMStorageType(Enum):

    """An enumeration of FSM storage types."""

    MEMORY = "memory"
    NATS = "nats"
    REDIS = "redis"


@dataclass
class BotProperties:

    """A class representing the bot properties."""

    parse_mode: Optional[str] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_sending_without_reply: Optional[bool] = None
    link_preview_is_disabled: Optional[bool] = None
    link_preview_prefer_small_media: Optional[bool] = None
    link_preview_prefer_large_media: Optional[bool] = None
    link_preview_show_above_text: Optional[bool] = None
    show_caption_above_media: Optional[bool] = None


@dataclass
class NatsFSMStorageSettings:

    """A class representing the settings for the Nats FSM storage."""

    kv_states: KeyValueConfig = field(
        default_factory=lambda: KeyValueConfig("fsm_states_tgbot"),
    )
    kv_data: KeyValueConfig = field(
        default_factory=lambda: KeyValueConfig("fsm_data_tgbot"),
    )
    create_nats_kv_buckets: bool = False


@dataclass
class RedisFSMStorageSettings:

    """A class representing the settings for the Redis FSM storage."""

    db: int = 2
    connection_kwargs: Optional[dict[str, Any]] = None


@dataclass
class FSMStorageSettings:

    """A class representing the settings for the FSM storage."""

    storage_type: FSMStorageType = FSMStorageType.NATS
    nats: NatsFSMStorageSettings = field(
        default_factory=lambda: NatsFSMStorageSettings(),
    )
    redis: RedisFSMStorageSettings = field(
        default_factory=lambda: RedisFSMStorageSettings(),
    )


@dataclass
class BotApiSettings:

    """A class representing the settings for a bot API."""

    type: BotApiType = BotApiType.OFFICIAL
    api_url: Optional[str] = None
    file_url: Optional[str] = None

    def is_local(self) -> bool:
        """
        Check if the bot API is local.

        Returns :
            bool: True if the bot API is local, False otherwise.
        """
        return self.type == BotApiType.LOCAL

    def create_server(self) -> TelegramAPIServer:
        if not self.is_local():
            raise RuntimeError(
                "Create a server only when you use a local Bot API server: https://core.telegram.org/bots/api#using-a-local-bot-api-server.",
            )
        return TelegramAPIServer(
            base=f"{self.api_url}/bot{{token}}/{{method}}",
            file=f"{self.file_url}/{{path}}",
            is_local=self.is_local(),
        )


@dataclass
class WebHookSettings:

    """A class representing a Webhook settings."""

    url: str
    secret_token: SecretStr
    webhook_path: str = "/webhook"

    @property
    def path(self) -> str:
        return f"/{self.webhook_path}" if not self.webhook_path.startswith("/") else self.webhook_path


@dataclass
class TelegramBot:

    """A class representing a Telegram bot settings."""

    token: SecretStr
    properties: BotProperties
    bot_api: BotApiSettings
    fsm_storage: FSMStorageSettings
    webhook: Optional[WebHookSettings] = None

    def create_session(self) -> Optional[BaseSession]:
        if self.bot_api.is_local():
            server = self.bot_api.create_server()
            return AiohttpSession(api=server)
        return None

    def create_bot_instance(self) -> Bot:
        session = self.create_session()
        return Bot(
            token=self.token.value,
            session=session,
            default=DefaultBotProperties(
                parse_mode=self.properties.parse_mode,
                disable_notification=self.properties.disable_notification,
                protect_content=self.properties.protect_content,
                allow_sending_without_reply=self.properties.allow_sending_without_reply,
                link_preview_is_disabled=self.properties.link_preview_is_disabled,
                link_preview_prefer_small_media=self.properties.link_preview_prefer_small_media,
                link_preview_prefer_large_media=self.properties.link_preview_prefer_large_media,
                link_preview_show_above_text=self.properties.link_preview_show_above_text,
                show_caption_above_media=self.properties.show_caption_above_media,
            ),
        )


def get_telegram_settings() -> list[Any]:
    """Returns a list of telegram bot settings classes."""
    return [
        TelegramBot,
        WebHookSettings,
        BotApiSettings,
        FSMStorageSettings,
        NatsFSMStorageSettings,
        RedisFSMStorageSettings,
    ]


__all__ = ["get_telegram_settings"]
