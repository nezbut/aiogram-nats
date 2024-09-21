from aiogram_nats.core.entities.mailing import Mailing
from aiogram_nats.core.interfaces.interfaces.mailing import MailingManager


class RemoveMailing:

    """Class is responsible for removing a mailing."""

    def __init__(self, mailing_manager: MailingManager) -> None:
        self.mailing_manager = mailing_manager

    async def __call__(self, mailing: Mailing) -> None:
        """
        Asynchronously removes a mailing.

        Args :
            mailing (Mailing): The mailing to be removed.

        Returns :
            None: This function does not return anything.
        """
        await self.mailing_manager.remove(mailing)
