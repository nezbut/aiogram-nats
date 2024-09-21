from dataclasses import dataclass
from uuid import UUID

from aiogram_nats.core.entities.scheduled import ScheduledEntity
from aiogram_nats.core.entities.user import User


@dataclass
class MailingMessage:

    """
    Represents a message in a mailing.

    Attributes :
        text (str): The text of the message.
        media_address (str): The address of the media.
    """

    text: str
    media_address: str


@dataclass
class Mailing:

    """
    Represents a mailing.

    Attributes :
        id (UUID): The ID of the mailing.
        users (list[User]): The list of users associated with the mailing.
        message (MailingMessage): The message of the mailing.
    """

    id: UUID
    users: list[User]
    message: MailingMessage


@dataclass
class ScheduledMailing(Mailing, ScheduledEntity):

    """
    A scheduled mailing entity that represents a mailing that is scheduled to be sent at a later time.

    Attributes :
        id (UUID): The unique identifier of the scheduled mailing.
        users (list[User]): The list of users associated with the mailing.
        message (MailingMessage): The message of the mailing.
        scheduled_time (datetime.datetime): The time at which the entity is scheduled.
    """

    pass
