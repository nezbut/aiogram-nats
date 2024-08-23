from dishka import Provider, Scope, provide

from aiogram_nats.core.interactors import mailing, messages


class InteractorsProvider(Provider):

    """Provider for interactors"""

    scope = Scope.REQUEST

    create_mailing = provide(mailing.CreateMailing)
    remove_mailing = provide(mailing.RemoveMailing)
    schedule_mailing = provide(mailing.ScheduleMailing)
    start_mailing = provide(mailing.StartMailing)

    schedule_message_deletion = provide(messages.ScheduleMessageDeletion)
    schedule_message_send = provide(messages.ScheduleMessageSend)
