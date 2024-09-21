from typing import Protocol

from aiogram_nats.core.entities.mailing import Mailing, MailingMessage
from aiogram_nats.core.entities.user import User


class MailingManager(Protocol):

    """Class is responsible for managing mailings."""

    async def create(self, message: MailingMessage, creator: User, users: list[User]) -> Mailing:
        """
        Asynchronously creates a new mailing.

        Args :
            message (MailingMessage): The message of the mailing.
            users (list[User]): The list of users associated with the mailing.
            creator (User): The creator of the mailing.

        Returns :
            Mailing: The newly created mailing.

        """
        raise NotImplementedError

    async def save(self, mailing: Mailing) -> None:
        """
        Asynchronously saves a mailing.

        Args :
            mailing (Mailing): The mailing to be saved.

        """
        raise NotImplementedError

    async def remove(self, mailing: Mailing) -> None:
        """
        Remove a mailing from the system.

        Args :
            mailing (Mailing): The mailing object to be removed.

        """
        raise NotImplementedError
