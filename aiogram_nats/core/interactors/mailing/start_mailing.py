from collections.abc import Awaitable, Callable
from typing import Any

from aiogram_nats.core.entities.mailing import Mailing, ScheduledMailing
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler


class StartMailing:

    """Class is responsible for starting a mailing."""

    def __init__(self, mailing_starter: Callable[[Mailing], Awaitable[Any]]) -> None:
        self.mailing_starter = mailing_starter

    async def __call__(self, mailing: Mailing) -> None:
        """
        Asynchronously starts a mailing.

        Args :
            mailing (Mailing): The mailing to be started.

        Returns :
            None: This function does not return anything.
        """
        await self.mailing_starter(mailing)


class ScheduleMailing:

    """Class is responsible for scheduling a mailing."""

    def __init__(self, scheduler: Scheduler) -> None:
        self.scheduler = scheduler

    async def __call__(self, mailing: ScheduledMailing) -> str:
        """
        Asynchronously schedules a mailing to be started at a later time.

        Args :
            mailing (ScheduledMailing): The mailing to be scheduled.

        Returns :
            str: The scheduling ID of the mailing.

        """
        return await self.scheduler.schedule_mailing(mailing)
