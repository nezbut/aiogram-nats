from collections.abc import Awaitable, Callable
from time import time
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update
from structlog.stdlib import BoundLogger

from aiogram_nats.tgbot.utils.data import MiddlewareData


class LoggingMiddleware(BaseMiddleware):

    """Logging middleware."""

    def __init__(self, logger: BoundLogger) -> None:
        self.logger = logger

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[Update, MiddlewareData], Awaitable[Any]],
        event: Update,
        data: MiddlewareData,
    ) -> Any:
        """Logging middleware."""
        data["logger"] = self.logger
        log_data = (
            event.update_id,
            event.event.__class__.__name__,
            data["event_from_user"].id,
            data["event_from_user"].is_bot,
        )

        await self.logger.ainfo("New Update: update_id=%d, event_name=%s, user_id=%d, is_bot=%s", *log_data)
        try:
            start_time = time()
            result = await handler(event, data)
            end_time = time()
            elapsed_time = end_time - start_time
            await self.logger.ainfo("Update is handled in %dms. update_id=%s", int(elapsed_time * 1000), event.update_id)
        except Exception as err:  # noqa: BLE001
            await self.logger.aexception("Error in the handler: %s. update_id=%s", err.__class__.__name__, event.update_id)
        else:
            return result
