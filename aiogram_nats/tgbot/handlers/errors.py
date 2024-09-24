from aiogram import Bot, Router
from aiogram.types.error_event import ErrorEvent

errors_router = Router()


@errors_router.error()
async def error_handle(event: ErrorEvent, bot: Bot) -> None:
    """Handler errors"""
    # logger.exception(
    #     "Cause unexpected exception %s, by processing %s",  # noqa: ERA001
    #     event.exception.__class__.__name__,
    #     event.update.model_dump(exclude_none=True),  # noqa: ERA001
    #     exc_info=event.exception, )
    ...
