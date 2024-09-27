from dataclasses import dataclass


@dataclass
class MailingServiceSettings:

    """Represents the settings for the mailing service."""

    main_subject: str = "service.mailing"
    service: str = "tgbot"
    stream_name: str = "mailing_stream"
    durable_name: str = "messages_manager"
