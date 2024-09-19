from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from aiogram_nats.core.interactors import mailing, messages
from aiogram_nats.infrastructure.clients.mailing_service import MailingServiceClient
from aiogram_nats.tgbot.mailing.manager import MailingManagerImpl
from aiogram_nats.tgbot.tasks import start_mailing
from aiogram_nats.tgbot.utils.data import MiddlewareData


class InteractorsMiddleware(BaseMiddleware):

    """Middleware for interactors."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Interactors Middleware"""
        container = data["dishka_container"]
        client = await container.get(MailingServiceClient)
        ctx = data["state"]
        holder = data["holder_dao"]
        manager = MailingManagerImpl(client, ctx, holder.user)

        data["create_mailing"] = mailing.CreateMailing(manager)
        data["remove_mailing"] = mailing.RemoveMailing(manager)
        data["start_mailing"] = mailing.StartMailing(start_mailing.kiq)

        data["schedule_mailing"] = await container.get(mailing.ScheduleMailing)
        data["schedule_send"] = await container.get(messages.ScheduleMessageSend)
        data["schedule_deletion"] = await container.get(messages.ScheduleMessageDeletion)

        return await handler(event, data)
