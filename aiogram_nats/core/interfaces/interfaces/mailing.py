from typing import Protocol

from aiogram_nats.core.entities.mailing import Mailing, MailingMessage
from aiogram_nats.core.entities.user import User


class MailingCreator(Protocol):

    """Protocol for creating a mailing."""

    async def create(self, message: MailingMessage, users: list[User]) -> Mailing:
        """
        Asynchronously creates a new mailing.

        Args :
            message (MailingMessage): The message of the mailing.
            users (list[User]): The list of users associated with the mailing.

        Returns :
            Mailing: The newly created mailing.

        """
        raise NotImplementedError


class MailingSaver(Protocol):

    """Protocol for saving a mailing."""

    async def save(self, mailing: Mailing) -> None:
        """
        Asynchronously saves a mailing.

        Args :
            mailing (Mailing): The mailing to be saved.

        """
        raise NotImplementedError


class MailingStarter(Protocol):

    """Protocol for starting a mailing."""

    async def start(self, mailing: Mailing) -> None:
        """
        Asynchronously starts a mailing.

        Args :
            mailing (Mailing): The mailing to be started.

        """
        raise NotImplementedError


class MailingRemover(Protocol):

    """Protocol for removing a mailing."""

    async def remove(self, mailing: Mailing) -> None:
        """
        Remove a mailing from the system.

        Args :
            mailing (Mailing): The mailing object to be removed.

        """
        raise NotImplementedError
