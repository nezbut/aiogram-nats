from aiogram_nats.core.entities.mailing import Mailing, ScheduledMailing
from aiogram_nats.core.interfaces.interfaces.mailing import MailingStarter
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler


class StartMailing:

    """Class is responsible for starting a mailing."""

    def __init__(self, mailing_starter: MailingStarter) -> None:
        self.mailing_starter = mailing_starter

    async def __call__(self, mailing: Mailing) -> None:
        """
        Asynchronously starts a mailing.

        Args :
            mailing (Mailing): The mailing to be started.

        Returns :
            None: This function does not return anything.
        """
        await self.mailing_starter.start(mailing)


class ScheduleMailing:

    """Class is responsible for scheduling a mailing."""

    def __init__(self, mailing_starter: MailingStarter, scheduler: Scheduler) -> None:
        self.mailing_starter = mailing_starter
        self.scheduler = scheduler

    async def __call__(self, mailing: ScheduledMailing) -> str:
        """
        Asynchronously schedules a mailing to be started at a later time.

        Args :
            mailing (ScheduledMailing): The mailing to be scheduled.

        Returns :
            str: The scheduling ID of the mailing.

        """
        starter = self.mailing_starter.start
        return await self.scheduler.schedule(mailing, starter)
