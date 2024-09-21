from typing import Any, TypeVar

import taskiq.scheduler.created_schedule
from taskiq import AsyncTaskiqDecoratedTask, ScheduleSource

from aiogram_nats.core.entities.mailing import ScheduledMailing
from aiogram_nats.core.entities.message import MessageDeletionScheduled, MessageSendScheduled
from aiogram_nats.core.entities.scheduled import ScheduledEntity
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler
from aiogram_nats.tgbot import tasks

ScheduledSupport = TypeVar("ScheduledSupport", bound=ScheduledEntity)


class SchedulerImpl(Scheduler):

    """
    Implementation of the Scheduler interface.

    This class provides an implementation of the Scheduler interface and
    allows you to schedule tasks to be executed at a later time.
    """

    def __init__(self, source: ScheduleSource) -> None:
        self.source = source

    async def _schedule(self, task: AsyncTaskiqDecoratedTask[[ScheduledSupport], Any], entity: ScheduledSupport) -> str:
        scheduled: taskiq.scheduler.created_schedule.CreatedSchedule = await task.schedule_by_time(
            self.source,
            entity.scheduled_time,
            entity,
        )
        return scheduled.schedule_id

    async def schedule_send_message(self, message: MessageSendScheduled) -> str:
        """
        Asynchronously schedules a task to send a message.

        :param message: The message to be sent.
        :type message: MessageSendScheduled

        :return: The scheduling ID of the send task.
        :rtype: str
        """
        return await self._schedule(tasks.send_message, message)

    async def schedule_delete_message(self, message: MessageDeletionScheduled) -> str:
        """
        Asynchronously schedules the deletion of a message.

        :param message: The message to be deleted.
        :type message: MessageDeletionScheduled

        :return: The scheduling ID of the deletion task.
        :rtype: str
        """
        return await self._schedule(tasks.remove_message, message)

    async def schedule_mailing(self, mailing: ScheduledMailing) -> str:
        """
        Asynchronously schedules a mailing to be started at a later time.

        :param mailing: The mailing to be scheduled.
        :type mailing: ScheduledMailing

        :return: The scheduling ID of the mailing.
        :rtype: str
        """
        return await self._schedule(tasks.start_mailing, mailing)
