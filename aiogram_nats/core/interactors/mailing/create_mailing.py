from aiogram_nats.core.entities.mailing import Mailing, MailingMessage
from aiogram_nats.core.entities.user import User
from aiogram_nats.core.interfaces.interfaces.mailing import MailingManager


class CreateMailing:

    """Class is responsible for creating a new mailing."""

    def __init__(self, mailing_manager: MailingManager) -> None:
        self.mailing_manager = mailing_manager

    async def __call__(self, message: MailingMessage, creator: User, users: list[User]) -> Mailing:
        """
        Asynchronously creates a new mailing.

        Args :
            message (MailingMessage): The message of the mailing.
            users (list[User]): The list of users associated with the mailing.

        Returns :
            Mailing: The newly created mailing.
        """
        mailing = await self.mailing_manager.create(message, creator, users)
        await self.mailing_manager.save(mailing)
        return mailing
