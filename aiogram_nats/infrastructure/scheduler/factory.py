from typing import cast

from taskiq import AsyncBroker, AsyncResultBackend, ScheduleSource
from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource

from aiogram_nats.common.settings import Settings
from aiogram_nats.common.settings.models.broker import BrokerSettings, TasksBrokerType
from aiogram_nats.infrastructure.scheduler.override import PullBasedJetStreamBrokerDI, PushBasedJetStreamBrokerDI


def create_tasks_broker(settings: BrokerSettings) -> AsyncBroker:
    """
    Creates a Tasks Broker based on the given Broker Settings.

    :param settings: (BrokerSettings): The broker settings containing the necessary information for creating the Tasks Broker.

    :return: (AsyncBroker): The created Tasks Broker.
    """
    nats_settings = settings.nats
    broker_type = PullBasedJetStreamBrokerDI if nats_settings.tasks.tasks_broker_type == TasksBrokerType.PULL else PushBasedJetStreamBrokerDI
    broker: AsyncBroker = cast(AsyncBroker, broker_type(
        [server.make_uri().value for server in nats_settings.servers],
        stream_config=nats_settings.tasks.tasks_stream_config,
        consumer_config=nats_settings.tasks.tasks_consumer_config,
        pull_consume_batch=nats_settings.tasks.pull_consume_batch,
        pull_consume_timeout=nats_settings.tasks.pull_consume_timeout,
        queue=nats_settings.tasks.queue,
        subject=nats_settings.tasks.subject,
    ))
    return broker


def create_tasks_result_backend(settings: Settings) -> AsyncResultBackend:
    """
    Creates an asynchronous result backend for taskiq based on the provided settings.

    :param settings: (Settings): The settings object containing the configuration for the result backend.

    :return: (AsyncResultBackend): The created asynchronous result backend.
    """
    redis_settings = settings.db.redis
    result_settings = redis_settings.tasks.result_backend

    result: RedisAsyncResultBackend = RedisAsyncResultBackend(
        redis_url=redis_settings.make_uri(db=result_settings.db).value,
        keep_results=result_settings.keep_results,
        result_ex_time=result_settings.result_ex_time,
        result_px_time=result_settings.result_px_time,
        max_connection_pool_size=result_settings.max_connection_pool_size,
        **result_settings.connection_kwargs,
    )
    return result


def create_schedule_source(settings: Settings) -> ScheduleSource:
    """
    Creates a schedule source based on the provided settings.

    :param settings: (Settings): The settings object containing the configuration for the schedule source.
    :return: (ScheduleSource): The created schedule source.
    """
    redis_settings = settings.db.redis
    source_settings = redis_settings.tasks.schedule_source

    source: RedisScheduleSource = RedisScheduleSource(
        url=redis_settings.make_uri(db=source_settings.db).value,
        prefix=source_settings.prefix,
        buffer_size=source_settings.buffer_size,
        max_connection_pool_size=source_settings.max_connection_pool_size,
        **source_settings.connection_kwargs,
    )
    return source
