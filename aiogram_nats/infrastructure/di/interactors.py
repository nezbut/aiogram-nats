from dishka import Provider, Scope, provide

from aiogram_nats.core.interactors import mailing


class InteractorsProvider(Provider):

    """Provider for interactors"""

    scope = Scope.REQUEST

    create_mailing = provide(mailing.CreateMailing)
    remove_mailing = provide(mailing.RemoveMailing)


def get_interactors_providers() -> list[Provider]:
    """Returns a list of interactors providers for di."""
    return [InteractorsProvider()]
