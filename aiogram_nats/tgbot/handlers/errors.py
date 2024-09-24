from aiogram import Bot, Router
from aiogram.types.error_event import ErrorEvent

errors_router = Router()


@errors_router.error()
async def error_handle(event: ErrorEvent, bot: Bot) -> None:
    # logger.exception(
    #     "Cause unexpected exception %s, by processing %s",
    #     event.exception.__class__.__name__,
    #     event.update.model_dump(exclude_none=True),
    #     exc_info=event.exception,
    # )
    ...
