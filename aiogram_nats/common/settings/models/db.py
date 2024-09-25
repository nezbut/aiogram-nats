from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from aiogram_nats.common.settings.models.security import SecretStr


@dataclass
class TasksScheduleSource:

    """Represents the settings for the tasks schedule source."""

    db: int = 4
    prefix: str = "schedule"
    buffer_size: int = 50
    max_connection_pool_size: int | None = None
    connection_kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass
class TasksResultBackend:

    """Represents the settings for the tasks result backend."""

    db: int = 5
    keep_results: bool = True
    result_ex_time: int | None = None
    result_px_time: int | None = None
    max_connection_pool_size: int | None = None
    connection_kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass
class TasksRedisSettings:

    """A dataclass representing the Redis settings for tasks."""

    schedule_source: TasksScheduleSource = field(
        default_factory=TasksScheduleSource)
    result_backend: TasksResultBackend = field(
        default_factory=TasksResultBackend)


@dataclass
class RedisSettings:

    """A class representing Redis settings."""

    uri: Optional[SecretStr] = None
    host: str = "localhost"
    port: int = 6379
    username: str = ""
    password: SecretStr = field(default_factory=lambda: SecretStr(value=""))
    db: int = 0
    ssl: bool = False
    tasks: TasksRedisSettings = field(default_factory=TasksRedisSettings)

    def make_uri(self, db: Optional[int] = None) -> SecretStr:
        """
        Creates a Redis connection URI based on the provided settings.

        :param db: (Optional[int]): The database number to connect to. If not provided, the default database number is used.

        :return: (SecretStr): The constructed Redis connection URI.

        """
        if uri := self.uri:
            return uri
        user_and_pass = f"{self.username}:{self.password.value}@"
        username_and_password = user_and_pass if self.username or self.password.value else ""
        db_num = self.db if db is None else db
        url = f"redi{'ss' if self.ssl else 's'}://{username_and_password}{self.host}:{self.port}/{db_num}"

        return SecretStr(value=url)


class DataBaseDialect(Enum):

    """An enumeration of supported database dialects."""

    POSTGRESQL = "postgresql"


@dataclass
class RDBSettings:

    """
    A class representing relational database settings.

    Attributes :
        uri (SecretStr): The database connection URI.
        dialect (DataBaseDialect): The database dialect.
        driver (str): The database driver.
        username (str): The database username.
        password (SecretStr): The database password.
        host (str): The database host.
        port (int): The database port.
        db_name (str): The database name.
        echo (bool): Whether to echo database queries.
    """

    uri: Optional[SecretStr] = None
    dialect: DataBaseDialect = DataBaseDialect.POSTGRESQL
    driver: str = "asyncpg"
    username: str = "postgres"
    password: SecretStr = field(
        default_factory=lambda: SecretStr(value="postgres"))
    host: str = "localhost"
    port: int = 5432
    db_name: str = "aiogram_nats"
    echo: bool = False

    def make_uri(self) -> SecretStr:
        """
        Creates a database connection URI based on the provided settings.

        Returns :
            SecretStr: The constructed database connection URI.

        Raises :
            ValueError: If a URI is not specified or the database is not supported
        """
        if uri := self.uri:
            return uri
        elif self.dialect == DataBaseDialect.POSTGRESQL:
            url = (
                f"{self.dialect.value}+{self.driver}://"
                f"{self.username}:{self.password.value}"
                f"@{self.host}:{self.port}/{self.db_name}"
            )
            return SecretStr(value=url)
        else:
            raise ValueError(
                "A uri is not specified or a database is not supported",
            )


@dataclass
class DBSettings:

    """
    A class representing database settings.

    Attributes :
        rdb (RDBSettings): The Relational Database settings.
        redis (RedisSettings): The Redis settings.
    """

    rdb: RDBSettings
    redis: RedisSettings
