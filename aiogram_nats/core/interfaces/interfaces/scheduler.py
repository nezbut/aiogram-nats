from typing import Protocol

from aiogram_nats.core.entities.mailing import ScheduledMailing
from aiogram_nats.core.entities.message import MessageDeletionScheduled, MessageSendScheduled


class Scheduler(Protocol):

    """A protocol for scheduling tasks."""

    async def schedule_delete_message(self, message: MessageDeletionScheduled) -> str:
        """
        Asynchronously schedules the deletion of a message.

        :param message: The message to be deleted.
        :type message: MessageDeletionScheduled

        :return: The scheduling ID of the deletion task.
        :rtype: str
        """
        raise NotImplementedError

    async def schedule_send_message(self, message: MessageSendScheduled) -> str:
        """
        Asynchronously schedules a task to send a message.

        :param message: The message to be sent.
        :type message: MessageSendScheduled

        :return: The scheduling ID of the send task.
        :rtype: str
        """
        raise NotImplementedError

    async def schedule_mailing(self, mailing: ScheduledMailing) -> str:
        """
        Asynchronously schedules a mailing to be started at a later time.

        :param mailing: The mailing to be scheduled.
        :type mailing: ScheduledMailing

        :return: The scheduling ID of the mailing.
        :rtype: str
        """
        raise NotImplementedError
