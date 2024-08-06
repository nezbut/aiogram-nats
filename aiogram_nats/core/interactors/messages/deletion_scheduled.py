from aiogram_nats.core.entities.message import MessageDeletionScheduled
from aiogram_nats.core.interfaces.interfaces.message_remover import MessageRemover
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler


class ScheduleMessageDeletion:

    """

    Class is responsible for scheduling the deletion of messages.

    Attributes :
        scheduler (Scheduler): The scheduler object used to schedule tasks.
        message_remover (MessageRemover): The message remover object used to remove messages.

    """

    def __init__(self, scheduler: Scheduler, remover: MessageRemover) -> None:
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
        task = self.message_remover.remove
        return await self.scheduler.schedule(message, task)
