from dishka import AsyncContainer, make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq_nats import PullBasedJetStreamBroker, PushBasedJetStreamBroker  # type: ignore[import-untyped]

from aiogram_nats.infrastructure.di.broker import get_broker_providers
from aiogram_nats.infrastructure.di.clients import get_clients_providers
from aiogram_nats.infrastructure.di.database import get_database_providers
from aiogram_nats.infrastructure.di.logs import get_logging_providers
from aiogram_nats.infrastructure.di.settings import get_settings_providers
from aiogram_nats.tgbot.di.bot import get_bot_providers
from aiogram_nats.tgbot.di.i18n import get_i18n_bot_providers


def _create_override_container() -> AsyncContainer:
    providers = [
        *get_database_providers(),
        *get_settings_providers(),
        *get_bot_providers(),
        *get_clients_providers(),
        *get_broker_providers(),
        *get_i18n_bot_providers(),
        *get_logging_providers(),
    ]
    return make_async_container(*providers)


class PullBasedJetStreamBrokerDI(
    PullBasedJetStreamBroker,  # type: ignore[no-any-unimported]
):

    """
    JetStream broker for pull based message consumption.

    It's named `pull` based because consumer requests messages,
    not NATS server sends them.
    """

    async def startup(self) -> None:
        """
        Startup event handler.

        It simply connects to NATS cluster, and
        setup JetStream.
        """
        container = _create_override_container()
        await super().startup()
        setup_dishka(container, self)


class PushBasedJetStreamBrokerDI(
    PushBasedJetStreamBroker,  # type: ignore[no-any-unimported]
):

    """
    JetStream broker for push based message consumption.

    It's named `push` based because nats server push messages to
    the consumer, not consumer requests them.
    """

    async def startup(self) -> None:
        """
        Startup event handler.

        It simply connects to NATS cluster, and
        setup JetStream.
        """
        container = _create_override_container()
        await super().startup()
        setup_dishka(container, self)
