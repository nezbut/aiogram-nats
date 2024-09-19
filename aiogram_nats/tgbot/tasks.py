import json
from collections.abc import AsyncGenerator
from typing import Any

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import Message
from dishka.integrations.taskiq import FromDishka as Depends
from dishka.integrations.taskiq import inject
from nats.aio.msg import Msg

from aiogram_nats.core.entities.mailing import Mailing, MediaContentType
from aiogram_nats.core.entities.message import MessageDeletionScheduled, MessageSendScheduled
from aiogram_nats.core.entities.user import User
from aiogram_nats.infrastructure.clients.mailing_service import MailingServiceClient
from aiogram_nats.infrastructure.scheduler.taskiq_constants import taskiq_broker


@taskiq_broker.task()
@inject
async def start_mailing(
    mailing: Mailing,
    client: Depends[MailingServiceClient],
    bot: Depends[Bot],
) -> None:
    """
    Asynchronously starts a mailing process.

    :param mailing: The mailing object containing the details of the mailing.
    :type mailing: Mailing

    :param client: The client for interacting with the mailing service.
    :type client: MailingServiceClient
    :param bot: The bot object for sending messages.
    :type bot: Bot

    :return:
    :rtype: None
    """
    async for msg in _get_mailing_messages(mailing, client):
        user = User(**json.loads(msg.data))
        try:
            if not mailing.message.media:
                await bot.send_message(chat_id=user.id, text=mailing.message.text)
                await msg.ack()
                continue

            media_address = mailing.message.media.address
            match mailing.message.media.media_type:
                case MediaContentType.PHOTO:
                    await bot.send_photo(chat_id=user.id, photo=media_address, caption=mailing.message.text)
                case MediaContentType.VIDEO:
                    await bot.send_video(chat_id=user.id, video=media_address, caption=mailing.message.text)
                case MediaContentType.AUDIO:
                    await bot.send_audio(chat_id=user.id, audio=media_address, caption=mailing.message.text)
                case MediaContentType.DOCUMENT:
                    await bot.send_document(chat_id=user.id, document=media_address, caption=mailing.message.text)

        except TelegramRetryAfter as e:
            # Limit exceeded, continue in: {e.retry_after} (add logging)
            await msg.nak(delay=e.retry_after)
            continue
        except TelegramForbiddenError:
            # User blocked Bot (add logging)
            pass
        await msg.ack()


async def _get_mailing_messages(mailing: Mailing, client: MailingServiceClient) -> AsyncGenerator[Msg, Any]:
    while msgs := await client.get_mailing_messages(str(mailing.id)):
        yield msgs[0]


@taskiq_broker.task()
@inject
async def remove_message(message: MessageDeletionScheduled, bot: Depends[Bot]) -> bool:
    """
    Removes a scheduled message deletion from a chat.

    :param message: The scheduled message deletion to remove.
    :type message: MessageDeletionScheduled
    :param bot: The bot instance to use for deletion.
    :type bot: Bot

    :return: Whether the message was successfully deleted.
    :rtype: bool
    """
    return await bot.delete_message(chat_id=message.user.id, message_id=message.id)


@taskiq_broker.task()
@inject
async def send_message(message: MessageSendScheduled, bot: Depends[Bot]) -> Message:
    """
    Sends a scheduled message to a user.

    :param message: The scheduled message to send.
    :type message: MessageSendScheduled
    :param bot: The bot instance to use for sending the message.
    :type bot: Bot

    :return: The sent message.
    :rtype: Message
    """
    return await bot.send_message(chat_id=message.user.id, text=message.text)
