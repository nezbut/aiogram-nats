from aiogram_nats.core.entities.mailing import Mailing
from aiogram_nats.core.interfaces.interfaces.mailing import MailingRemover


class RemoveMailing:

    """Class is responsible for removing a mailing."""

    def __init__(self, mailing_remover: MailingRemover) -> None:
        self.mailing_remover = mailing_remover

    async def __call__(self, mailing: Mailing) -> None:
        """
        Asynchronously removes a mailing.

        Args :
            mailing (Mailing): The mailing to be removed.

        Returns :
            None: This function does not return anything.
        """
        await self.mailing_remover.remove(mailing)
