from typing import Final

from taskiq import AsyncBroker, TaskiqScheduler

from aiogram_nats.common.settings import Settings
from aiogram_nats.infrastructure.scheduler.factory import (
    create_schedule_source,
    create_tasks_broker,
    create_tasks_result_backend,
)

_settings = Settings.from_dynaconf()

_result_backend = create_tasks_result_backend(_settings)
_schedule_source = create_schedule_source(_settings)

taskiq_broker: Final[AsyncBroker] = create_tasks_broker(
    _settings.broker,
).with_result_backend(_result_backend)

taskiq_scheduler: Final[TaskiqScheduler] = TaskiqScheduler(
    broker=taskiq_broker,
    sources=[_schedule_source],
)


__all__ = ["taskiq_broker", "taskiq_scheduler"]
