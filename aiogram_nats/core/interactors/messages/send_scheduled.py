from aiogram_nats.core.entities.message import MessageSendScheduled
from aiogram_nats.core.interfaces.interfaces.message_sender import MessageSender
from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler


class ScheduleMessageSend:

    """
    Class responsible for scheduling the sending of messages.

    Args :
        scheduler (Scheduler): The scheduler instance to use for scheduling.
        message_sender (MessageSender): The message sender instance to use for sending messages.

    """

    def __init__(self, scheduler: Scheduler, message_sender: MessageSender) -> None:
        self.scheduler = scheduler
        self.message_sender = message_sender

    async def __call__(self, message: MessageSendScheduled) -> None:
        """
        Asynchronously schedules a task to send a scheduled message.

        Args :
            message (MessageSendScheduled): The scheduled message to send.

        Returns :
            None
        """
        task = self.message_sender.send
        await self.scheduler.schedule(message, task)
