from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from nats.aio.client import Client
from nats.js import JetStreamContext

from aiogram_nats.common.log.installer import LoggersInstaller
from aiogram_nats.common.settings.models.mailing_service import MailingServiceSettings
from aiogram_nats.infrastructure.clients.mailing_service import MailingServiceClient


class ClientsProvider(Provider):

    """Clients provider."""

    scope = Scope.APP

    @provide
    async def get_mailing_service_client(
        self,
        settings: MailingServiceSettings,
        js: JetStreamContext,
        nc: Client,
        installer: LoggersInstaller,
    ) -> AsyncIterable[MailingServiceClient]:
        """Provides a MailingServiceClient instance."""
        async with MailingServiceClient(
            nats_client=nc,
            mailing_service_settings=settings,
            js=js,
            logging=installer,
        ) as client:
            yield client


def get_clients_providers() -> list[Provider]:
    """Returns a clients providers for di."""
    return [
        ClientsProvider(),
    ]
