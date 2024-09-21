from aiogram_nats.core.entities.message import MessageDeletionScheduled, MessageSendScheduled
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler


class ScheduleMessageSend:

    """
    Class responsible for scheduling the sending of messages.

    Args :
        scheduler (Scheduler): The scheduler instance to use for scheduling.
    """

    def __init__(self, scheduler: Scheduler) -> None:
        self.scheduler = scheduler

    async def __call__(self, message: MessageSendScheduled) -> str:
        """
        Asynchronously schedules a task to send a scheduled message.

        Args :
            message (MessageSendScheduled): The scheduled message to send.

        Returns :
            None
        """
        return await self.scheduler.schedule_send_message(message)


class ScheduleMessageDeletion:

    """

    Class is responsible for scheduling the deletion of messages.

    Attributes :
        scheduler (Scheduler): The scheduler object used to schedule tasks.
    """

    def __init__(self, scheduler: Scheduler) -> None:
        self.scheduler = scheduler

    async def __call__(self, message: MessageDeletionScheduled) -> str:
        """
        Asynchronously calls the scheduled message deletion.

        Args :
            message (MessageDeletionScheduled): The message to be deleted.

        Returns :
            str: The scheduling ID of the deletion task.
        """
        return await self.scheduler.schedule_delete_message(message)
