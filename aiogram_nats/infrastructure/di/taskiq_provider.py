
from dishka import Provider, Scope, provide
from taskiq import AsyncBroker, AsyncResultBackend, ScheduleSource

from aiogram_nats.core.interfaces.interfaces.scheduler import Scheduler
from aiogram_nats.infrastructure.scheduler.impl import SchedulerImpl
from aiogram_nats.infrastructure.scheduler.taskiq_constants import taskiq_broker, taskiq_scheduler


class TaskiqProvider(Provider):

    """Provider for Taskiq."""

    scope = Scope.APP

    @provide
    async def get_broker(self) -> AsyncBroker:
        """Get the broker instance."""
        return taskiq_broker

    @provide
    async def get_schedule_source(self) -> ScheduleSource:
        """Get the schedule source instance."""
        return taskiq_scheduler.sources[0]

    @provide
    async def get_result_backend(self) -> AsyncResultBackend:
        """Get the result backend instance."""
        return taskiq_broker.result_backend


class SchedulerProvider(Provider):

    """Provider for Scheduler."""

    scope = Scope.APP

    scheduler = provide(SchedulerImpl, provides=Scheduler)


def get_taskiq_providers() -> list[Provider]:
    """Returns a list of taskiq providers for di."""
    return [
        TaskiqProvider(),
        SchedulerProvider(),
    ]
