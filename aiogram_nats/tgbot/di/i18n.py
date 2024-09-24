from dishka import Provider, Scope, provide
from fluentogram import TranslatorHub

from aiogram_nats.tgbot.i18n.factory import get_translator_hub


class I18NProvider(Provider):

    """A provider for the i18n."""

    scope = Scope.APP

    @provide
    def get_hub(self) -> TranslatorHub:
        """Provides a i18n"""
        return get_translator_hub(root_locale="ru")


def get_i18n_bot_providers() -> list[Provider]:
    """Returns a list of providers for the i18n."""
    return [
        I18NProvider(),
    ]
