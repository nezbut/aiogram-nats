from typing import Protocol

from aiogram_nats.core.entities.message import MessageSendScheduled


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
