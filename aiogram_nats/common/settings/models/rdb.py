from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from aiogram_nats.common.settings.models.security import SecretStr


class DataBaseDialect(Enum):

    """An enumeration of supported database dialects."""

    POSTGRESQL = "postgresql"


@dataclass
class DBSettings:

    """
    A class representing database settings.

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
    password: SecretStr = field(default_factory=lambda: SecretStr(value=""))
    host: str = "localhost"
    port: int = 5432
    db_name: str = "aiogram_nats"
    echo: bool = False

    def make_uri(self) -> SecretStr:
        """
        Creates a database connection URI based on the provided settings.

        If a URI is explicitly specified, it is returned as is. Otherwise, the function attempts to construct a URI
        for a PostgreSQL database using the provided dialect, driver, username, password, host, port, and database name.

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
