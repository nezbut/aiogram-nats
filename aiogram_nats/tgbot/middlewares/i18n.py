import logging
from collections.abc import Awaitable, Callable
from typing import Any, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub

from aiogram_nats.tgbot.utils.data import MiddlewareData

logger = logging.getLogger(__name__)


class I18NMiddleware(BaseMiddleware):

    """I18N middleware."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """I18N middleware."""
        user: Optional[User] = data.get("event_from_user")

        if user is None or not user.language_code:
            return await handler(event, data)

        container = data["dishka_container"]
        hub: TranslatorHub = await container.get(TranslatorHub)
        translator = hub.get_translator_by_locale(locale=user.language_code)
        data["i18n"] = translator
        data["i18n_getter"] = translator.get

        return await handler(event, data)
