from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from nats.js.api import ConsumerConfig, StreamConfig

from aiogram_nats.common.settings.models.security import SecretStr


class TasksBrokerType(Enum):

    """An enumeration representing the type of tasks broker."""

    PUSH = "push"
    PULL = "pull"


@dataclass
class TasksNatsSettings:

    """A dataclass representing the settings for the tasks NATS broker."""

    tasks_broker_type: TasksBrokerType = TasksBrokerType.PULL
    tasks_stream_config: StreamConfig = field(
        default_factory=lambda: StreamConfig("tasks_stream"),
    )
    tasks_consumer_config: ConsumerConfig = field(
        default_factory=lambda: ConsumerConfig(durable_name="tasks_consumer"),
    )
    pull_consume_batch: int = 1
    pull_consume_timeout: Optional[float] = None
    queue: Optional[str] = None
    subject: str = "tasks"


@dataclass
class NatsServerSettings:

    """A class representing NATS Server Settings."""

    uri: Optional[SecretStr] = None
    host: str = "localhost"
    port: int = 4222
    username: str = ""
    password: SecretStr = field(default_factory=lambda: SecretStr(value=""))

    def make_uri(self) -> SecretStr:
        """
        Creates a NATS connection URI based on the provided settings.

        Returns :
            SecretStr: The constructed NATS connection URI.
        """
        if uri := self.uri:
            return uri
        user_and_pass = f"{self.username}:{self.password.value}@"
        username_and_password = user_and_pass if self.username or self.password.value else ""
        url = f"nats://{username_and_password}{self.host}:{self.port}"
        return SecretStr(value=url)


@dataclass
class NatsSettings:

    """A class representing NATS Settings."""

    tasks: TasksNatsSettings = field(
        default_factory=lambda: TasksNatsSettings())
    servers: list[NatsServerSettings] = field(
        default_factory=lambda: [NatsServerSettings()])


@dataclass
class BrokerSettings:

    """A class representing broker settings."""

    nats: NatsSettings
