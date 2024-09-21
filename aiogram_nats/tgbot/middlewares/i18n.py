import logging
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from aiogram_nats.tgbot.utils.data import MiddlewareData

if TYPE_CHECKING:
    from fluentogram import TranslatorHub

logger = logging.getLogger(__name__)


class TranslatorRunnerMiddleware(BaseMiddleware):

    """Translator runner middleware."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Get Translator."""
        user: Optional[User] = data.get("event_from_user")

        if user is None or not user.language_code:
            return await handler(event, data)

        hub: TranslatorHub = data["translator_hub"]
        data["i18n"] = hub.get_translator_by_locale(locale=user.language_code)

        return await handler(event, data)
