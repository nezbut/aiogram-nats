from dataclasses import dataclass
from typing import Any


@dataclass
class MailingServiceSettings:

    """Represents the settings for the mailing service."""

    main_subject: str = "service.mailing"
    service: str = "tgbot"
    stream_name: str = "mailing_stream"


def get_mailing_service_settings() -> list[Any]:
    """Returns a list of mailing service settings classes."""
    return [
        MailingServiceSettings,
    ]


__all__ = ["get_mailing_service_settings"]
