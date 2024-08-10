from aiogram_nats.core.entities.mailing import Mailing, MailingMessage
from aiogram_nats.core.entities.user import User
from aiogram_nats.core.interfaces.interfaces.mailing import MailingCreator, MailingSaver


class CreateMailing:

    """Class is responsible for creating a new mailing."""

    def __init__(self, mailing_saver: MailingSaver, mailing_creator: MailingCreator) -> None:
        self.mailing_saver = mailing_saver
        self.mailing_creator = mailing_creator

    async def __call__(self, message: MailingMessage, users: list[User]) -> Mailing:
        """
        Asynchronously creates a new mailing.

        Args :
            message (MailingMessage): The message of the mailing.
            users (list[User]): The list of users associated with the mailing.

        Returns :
            Mailing: The newly created mailing.
        """
        mailing = await self.mailing_creator.create(message, users)
        await self.mailing_saver.save(mailing)
        return mailing
