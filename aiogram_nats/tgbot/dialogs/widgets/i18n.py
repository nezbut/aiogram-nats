from typing import cast

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

from aiogram_nats.tgbot.utils.data import MiddlewareData


class I18NWidget(Text):

    """A I18 widget."""

    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        middleware_data = cast(MiddlewareData, manager.middleware_data)
        i18n_getter = middleware_data["i18n_getter"]

        return i18n_getter(self.key, **data)
