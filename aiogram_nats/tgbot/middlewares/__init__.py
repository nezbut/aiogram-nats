from aiogram import Dispatcher

# from aiogram_dialog.api.protocols import BgManagerFactory  # noqa: ERA001
from aiogram_nats.common.settings import Settings
from aiogram_nats.tgbot.middlewares.i18n import TranslatorRunnerMiddleware
from aiogram_nats.tgbot.middlewares.init import InitMiddleware
from aiogram_nats.tgbot.middlewares.interactors import InteractorsMiddleware


def setup(
    dp: Dispatcher,
    # bg_manager_factory: BgManagerFactory,
    settings: Settings,
) -> None:
    """Setup middlewares."""
    dp.update.outer_middleware(
        InitMiddleware(
            # bg_manager_factory=bg_manager_factory,  # noqa: ERA001
            settings=settings,
        ),
    )
    dp.update.middleware(
        TranslatorRunnerMiddleware(),
    )
    dp.update.middleware(
        InteractorsMiddleware(),
    )
