import json
from typing import Any, Optional, Self

from aiogram.filters.state import StateType
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    DefaultKeyBuilder,
    KeyBuilder,
    StorageKey,
)
from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.errors import NotFoundError
from nats.js.kv import KeyValue

from aiogram_nats.common.settings.models.telegram import NatsFSMStorageSettings


class NatsStorage(BaseStorage):

    """A class representing the Nats FSM storage."""

    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        nats_storage_settings: NatsFSMStorageSettings,
        key_builder: Optional[KeyBuilder] = None,
    ) -> None:

        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.nc = nc
        self.js = js
        self.storage_settings = nats_storage_settings
        self._key_builder = key_builder
        self.kv_data: KeyValue
        self.kv_states: KeyValue

    async def create_storage(self) -> Self:
        """Asynchronously creates the storage for the Nats FSM."""
        self.kv_states = await self._get_kv_states()
        self.kv_data = await self._get_kv_data()
        return self

    async def _get_kv_states(self) -> KeyValue:
        return await self.js.create_key_value(config=self.storage_settings.kv_states)

    async def _get_kv_data(self) -> KeyValue:
        return await self.js.create_key_value(config=self.storage_settings.kv_data)

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        """
        Set state for specified key

        :param key: storage key
        :param state: new state
        """
        state = state.state if isinstance(state, State) else state
        key_ = self._key_builder.build(key)
        await self.kv_states.put(key_, self._dump(state or None))

    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Get key state

        :param key: storage key
        :return: current state
        """
        try:
            entry = await self.kv_states.get(self._key_builder.build(key))
            data = self._load(entry.value) if entry.value else None
            return data if isinstance(data, str) else None
        except NotFoundError:
            return None

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        """
        Write data (replace)

        :param key: storage key
        :param data: new data
        """
        key_ = self._key_builder.build(key)
        await self.kv_data.put(key_, self._dump(data))

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        """
        Get current data for key

        :param key: storage key
        :return: current data
        """
        try:
            entry = await self.kv_data.get(self._key_builder.build(key))
            data = self._load(entry.value) if entry.value else {}
            return data if isinstance(data, dict) else {}
        except NotFoundError:
            return {}

    async def close(self) -> None:
        """Closes the NATS connection."""
        pass

    @staticmethod
    def _dump(obj: Any) -> bytes:
        return json.dumps(obj).encode(encoding="utf-8")

    @staticmethod
    def _load(obj: bytes) -> Any:
        return json.loads(obj)
