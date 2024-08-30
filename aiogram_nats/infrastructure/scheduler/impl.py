from typing import Any

import taskiq.scheduler.created_schedule
from taskiq import AsyncBroker, ScheduleSource

from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler, SupportScheduled, Task


class SchedulerImpl(Scheduler):

    """
    Implementation of the Scheduler interface.

    This class provides an implementation of the Scheduler interface and
    allows you to schedule tasks to be executed at a later time.
    """

    def __init__(self, broker: AsyncBroker, source: ScheduleSource) -> None:
        self.broker = broker
        self.source = source
        self._labels: dict[str, Any] = {}

    async def schedule(self, entity: SupportScheduled, task: Task) -> str:
        """
        Schedule a task to be executed at a later time.

        :param entity: (SupportScheduled): The entity to be scheduled.
        :param task: (Task): The task to be executed. It should take a `SupportScheduled` object and return an `Awaitable` object.

        :return: (str): The scheduling ID.
        """
        reg_task = self.broker.register_task(task)
        scheduled: taskiq.scheduler.created_schedule.CreatedSchedule = await reg_task.schedule_by_time(
            self.source,
            entity.scheduled_time,
            entity,
        )
        return scheduled.schedule_id

    def add_labels(self, labels: dict[str, Any]) -> None:
        """
        Update the labels of the SchedulerImpl instance with the provided dictionary.

        :param labels: (dict[str, Any]): A dictionary containing the labels to be added.

        :return: (None)
        """
        self._labels.update(labels)
