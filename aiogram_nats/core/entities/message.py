from dataclasses import dataclass

from aiogram_nats.core.entities.scheduled import ScheduledEntity
from aiogram_nats.core.entities.user import User


@dataclass
class Message:

    """
    Represents a message in the system.

    Attributes :
        id (str): The unique identifier of the message.
        user (User): The user who sent the message.

    """

    id: str
    user: User


@dataclass
class MessageDeletionScheduled(Message, ScheduledEntity):

    """Represents a scheduled deletion of a message in the system."""

    pass


@dataclass
class MessageSendScheduled(Message, ScheduledEntity):

    """
    Represents a send message in the system.

    Attributes :
        media_address (str): The address of the media.
        text (str): The text of the message.
    """

    media_address: str
    text: str
