import secrets
from typing import Any, Optional

from aiogram import Bot

from aiogram_nats.tgbot.webhook.fastapi.handlers.base import BaseRequestHandler


class SimpleRequestHandler(BaseRequestHandler):

    """
    Handler for single Bot instance

    :param dispatcher: instance of :class:`aiogram.dispatcher.dispatcher.Dispatcher`
    :param handle_in_background: immediately responds to the Telegram instead of
        a waiting end of handler process
    :param bot: instance of :class:`aiogram.client.bot.Bot`
    :param secret_token: secret token for webhook
    """

    def __init__(
        self,
        handle_in_background: Optional[bool] = None,
        secret_token: Optional[str] = None,
        **data: Any,
    ) -> None:

        super().__init__(handle_in_background=handle_in_background, **data)
        self.secret_token = secret_token

    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        """
        Verifies the secret token of a Telegram webhook.

        :param telegram_secret_token: The secret token provided by Telegram.
        :param bot: The Bot instance associated with the webhook.
        :return: True if the secret token is valid, False otherwise.
        """
        if self.secret_token:
            return secrets.compare_digest(telegram_secret_token, self.secret_token)
        return True
