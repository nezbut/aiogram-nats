from aiogram import Dispatcher
from aiogram_dialog.api.protocols import BgManagerFactory
from structlog.stdlib import BoundLogger

from aiogram_nats.common.settings import Settings
from aiogram_nats.tgbot.middlewares.i18n import I18NMiddleware
from aiogram_nats.tgbot.middlewares.init import InitMiddleware
from aiogram_nats.tgbot.middlewares.interactors import InteractorsMiddleware
from aiogram_nats.tgbot.middlewares.logs import LoggingMiddleware


def setup(
    dp: Dispatcher,
    bg_manager_factory: BgManagerFactory,
    settings: Settings,
    logger: BoundLogger,
) -> None:
    """Setup middlewares."""
    dp.update.outer_middleware(
        InitMiddleware(
            bg_manager_factory=bg_manager_factory,
            settings=settings,
        ),
    )
    dp.update.middleware(
        I18NMiddleware(),
    )
    dp.update.middleware(
        InteractorsMiddleware(),
    )
    dp.update.outer_middleware(
        LoggingMiddleware(
            logger=logger,
        ),
    )
