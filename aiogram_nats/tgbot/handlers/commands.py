from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from aiogram_nats.tgbot.dialogs.states.menu import MainMenu

commands_router = Router()


@commands_router.message(CommandStart())
async def start_command(_: Message, dialog_manager: DialogManager) -> None:
    return await dialog_manager.start(MainMenu.menu, mode=StartMode.RESET_STACK)
