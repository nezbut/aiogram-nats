from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:

    """
    Represents a user in the system.

    Attributes :
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        joined_us (datetime): The datetime when the user joined.
        first_name (Optional[str]): The first name of the user.
        last_name (Optional[str]): The last name of the user.
    """

    id: int
    first_name: str
    joined_us: datetime
    username: Optional[str] = None
    last_name: Optional[str] = None

    @property
    def name(self) -> str:
        """
        Returns the full name of the user.

        If both the first name and last name are provided, it returns a string with the format "{first_name} {last_name}".
        Otherwise, it returns the username.

        :return: str
            The full name of the user.
        """
        if username := self.username:
            return username
        elif self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name
