from aiogram.fsm.state import State, StatesGroup


class MainMenu(StatesGroup):

    """A states group for the main menu."""

    menu = State()
