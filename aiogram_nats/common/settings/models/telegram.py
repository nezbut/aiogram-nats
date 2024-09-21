from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

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


@dataclass
class FSMStorageSettings:

    """A class representing the settings for the FSM storage."""

    kv_states: KeyValueConfig = field(default_factory=lambda: KeyValueConfig("fsm_states_tgbot"))
    kv_data: KeyValueConfig = field(default_factory=lambda: KeyValueConfig("fsm_data_tgbot"))


@dataclass
class BotApiSettings:

    """A class representing the settings for a bot API."""

    type: BotApiType = BotApiType.OFFICIAL

    def is_local(self) -> bool:
        """
        Check if the bot API is local.

        Returns :
            bool: True if the bot API is local, False otherwise.
        """
        return self.type == BotApiType.LOCAL


@dataclass
class WebHookSettings:

    """A class representing a Webhook settings."""

    url: str
    secret_token: SecretStr
    path: str


@dataclass
class TelegramBot:

    """A class representing a Telegram bot settings."""

    token: SecretStr
    bot_api: BotApiSettings
    fsm_storage: FSMStorageSettings
    webhook: Optional[WebHookSettings] = None


def get_telegram_settings() -> list[Any]:
    """Returns a list of telegram bot settings classes."""
    return [
        TelegramBot,
        WebHookSettings,
        BotApiSettings,
        FSMStorageSettings,
    ]


__all__ = ["get_telegram_settings"]
