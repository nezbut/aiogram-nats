from typing import Protocol

from aiogram_nats.core.entities.message import MessageDeletionScheduled, MessageSendScheduled


class MessageRemover(Protocol):

    """
    Class represents a message remover.

    It provides a method to remove a message from the system.
    """

    async def remove(self, message: MessageDeletionScheduled) -> None:
        """Removes a message from the system."""
        raise NotImplementedError


class MessageSender(Protocol):

    """
    Class represents a message sender.

    It provides a method to send a message.
    """

    async def send(self, message: MessageSendScheduled) -> None:
        """
        Asynchronously sends a scheduled message.

        Args :
            message (MessageSendScheduled): The scheduled message to send.

        Returns :
            None

        """
        raise NotImplementedError
