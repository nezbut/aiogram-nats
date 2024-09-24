from aiogram_dialog import Dialog, Window

from aiogram_nats.tgbot.dialogs.routers.globals.getters import get_user
from aiogram_nats.tgbot.dialogs.states import menu
from aiogram_nats.tgbot.dialogs.widgets.i18n import I18NWidget

menu_dialog = Dialog(
    Window(
        I18NWidget("hello-user"),
        state=menu.MainMenu.menu,
        getter=get_user,
    ),
)
