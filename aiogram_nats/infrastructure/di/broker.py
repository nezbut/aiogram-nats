from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from nats import connect
from nats.aio.client import Client
from nats.js import JetStreamContext

from aiogram_nats.common.settings.models.broker import NatsSettings


class NatsProvider(Provider):

    """Provider for Nats."""

    scope = Scope.APP

    @provide
    async def get_client(self, settings: NatsSettings) -> AsyncIterable[Client]:
        """Get Nats Client"""
        servers = [server.make_uri().value for server in settings.servers]
        async with await connect(servers) as nc:
            yield nc

    @provide
    async def get_js(self, client: Client) -> JetStreamContext:
        """Get JetStream context"""
        return client.jetstream()


def get_broker_providers() -> list[Provider]:
    """Returns a nats providers for di."""
    return [
        NatsProvider(),
    ]