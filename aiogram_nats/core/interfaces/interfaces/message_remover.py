from typing import Protocol

from aiogram_nats.core.entities.message import MessageDeletionScheduled


class MessageRemover(Protocol):

    """
    Class represents a message remover.

    It provides a method to remove a message from the system.
    """

    async def remove(self, message: MessageDeletionScheduled) -> None:
        """Removes a message from the system."""
        raise NotImplementedError
