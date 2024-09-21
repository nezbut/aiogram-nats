from aiogram_nats.core.entities.message import MessageDeletionScheduled, MessageSendScheduled
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler, Task


class ScheduleMessageSend:

    """
    Class responsible for scheduling the sending of messages.

    Args :
        scheduler (Scheduler): The scheduler instance to use for scheduling.
        message_sender (Task): The message sender instance to use for sending messages.

    """

    def __init__(self, scheduler: Scheduler, message_sender: Task) -> None:
        self.scheduler = scheduler
        self.message_sender = message_sender

    async def __call__(self, message: MessageSendScheduled) -> str:
        """
        Asynchronously schedules a task to send a scheduled message.

        Args :
            message (MessageSendScheduled): The scheduled message to send.

        Returns :
            None
        """
        return await self.scheduler.schedule(message, self.message_sender)


class ScheduleMessageDeletion:

    """

    Class is responsible for scheduling the deletion of messages.

    Attributes :
        scheduler (Scheduler): The scheduler object used to schedule tasks.
        message_remover (Task): The message remover object used to remove messages.

    """

    def __init__(self, scheduler: Scheduler, remover: Task) -> None:
        self.scheduler = scheduler
        self.message_remover = remover

    async def __call__(self, message: MessageDeletionScheduled) -> str:
        """
        Asynchronously calls the scheduled message deletion.

        Args :
            message (MessageDeletionScheduled): The message to be deleted.

        Returns :
            str: The scheduling ID of the deletion task.

        Raises :
            None.
        """
        return await self.scheduler.schedule(message, self.message_remover)
