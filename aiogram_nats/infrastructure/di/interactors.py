from dishka import Provider, Scope, provide

from aiogram_nats.core.interactors import mailing, messages


class InteractorsProvider(Provider):

    """Provider for interactors"""

    scope = Scope.REQUEST

    schedule_mailing = provide(mailing.ScheduleMailing)
    message_send = provide(messages.ScheduleMessageSend)
    message_deletion = provide(messages.ScheduleMessageDeletion)


def get_interactors_providers() -> list[Provider]:
    """Returns a list of interactors providers for di."""
    return [InteractorsProvider()]
