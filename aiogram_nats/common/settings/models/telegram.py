from dataclasses import dataclass
from enum import Enum
from typing import Optional

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
    webhook: Optional[WebHookSettings] = None
