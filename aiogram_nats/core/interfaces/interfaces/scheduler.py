from collections.abc import Awaitable, Callable
from typing import Any, Protocol, TypeVar

from aiogram_nats.core.entities.scheduled import ScheduledEntity

SupportScheduled = TypeVar("SupportScheduled", bound=ScheduledEntity)
Task = Callable[[SupportScheduled], Awaitable[Any]]


class Scheduler(Protocol):

    """

    A protocol for scheduling tasks.

    This class defines the interface for scheduling tasks. It has one method, which takes an `entity` and a `task` as arguments and returns a scheduling ID.

    """

    async def schedule(self, entity: SupportScheduled, task: Task) -> str:
        """
        Schedules a task to be executed at a later time.

        Args :
            entity (SupportScheduled): The entity to be
             scheduled
            task (Callable[[SupportScheduled, Any], Awaitable[Any]]): The task to be executed. It should take a `ScheduledEntity` object and any other arguments
            and return an `Awaitable` object.

        Returns :
            str: The scheduling ID.

        """
        raise NotImplementedError
