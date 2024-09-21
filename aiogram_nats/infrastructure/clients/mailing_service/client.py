import json
from typing import Any

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.errors import TimeoutError
from nats.js import JetStreamContext

from aiogram_nats.common.settings.models.mailing_service import MailingServiceSettings


class MailingServiceClient:

    """Represents a client for interacting with the mailing service."""

    def __init__(
            self,
            nats_client: Client,
            messages_psub: JetStreamContext.PullSubscription,
            mailing_service_settings: MailingServiceSettings,
            js: JetStreamContext,
    ) -> None:
        self._nc = nats_client
        self._psub = messages_psub
        self._js = js
        self._subject = f"{mailing_service_settings.main_subject}.{mailing_service_settings.service}"
        self._settings = mailing_service_settings

    async def get_mailing_messages(self, mailing_id: str, batch: int = 1, timeout: int = 5) -> list[Msg]:
        """
        Asynchronously retrieves a list of mailing messages for a given mailing ID.

        :param mailing_id: (str): The ID of the mailing.
        :param batch: (int): An integer representing the number of messages to retrieve in each batch. Defaults to 1.
        :param timeout: (int): An integer representing the maximum time to wait for a response from the server. Defaults to 5.

        :return: (list[Msg]): A list of Msg objects.
        """
        return await self._get_mailing_messages(mailing_id, batch, timeout)

    async def get_all_mailing_messages(self, mailing_id: str, timeout: int = 5) -> list[Msg]:
        """
        Asynchronously retrieves all mailing messages for a given mailing ID.

        :param mailing_id: (str): The ID of the mailing.
        :param timeout: (int): An integer representing the maximum time to wait for a response from the server. Defaults to 5.

        :return: (list[Msg]): A list of Msg objects.
        """
        stream_info = await self._js.stream_info(self._settings.stream_name)
        batch = stream_info.state.messages
        return await self._get_mailing_messages(mailing_id, batch=batch, timeout=timeout)

    async def create_mailing(self, payload_array: list[Any], timeout: float = 0.5) -> str:
        """
        Asynchronously creates a new mailing by sending a request to the NATS server.

        :param payload_array: (list[Any]): A list of payloads to be included in the mailing.
        :param timeout: (float, optional): The maximum time to wait for a response from the NATS server. Defaults to 0.5.

        :return: (str): The response from the NATS server as a decoded string.
        """
        payload = self._get_payload(payload_array)
        response = await self._nc.request(self._subject, payload, timeout=timeout)
        return response.data.decode(encoding="utf-8")

    async def delete_mailing(self, mailing_id: str) -> None:
        """
        Deletes a mailing by publishing a message to the delete subject with the given mailing ID.

        :param mailing_id: (str): The ID of the mailing to be deleted.

        :return: (None)
        """
        payload = self._get_payload(mailing_id)
        await self._nc.publish(f"{self._subject}.delete", payload)

    async def _get_mailing_messages(self, mailing_id: str, batch: int = 1, timeout: int = 5) -> list[Msg]:
        try:
            msgs = await self._psub.fetch(batch=batch, timeout=timeout)
        except TimeoutError:
            return []
        else:
            messages: list[Msg] = [
                msg for msg in msgs if msg.headers and msg.headers.get("Mailing-Id") == mailing_id
            ]
            return messages

    @staticmethod
    def _get_payload(obj: Any) -> bytes:
        payload = json.dumps(obj)
        return payload.encode(encoding="utf-8")
