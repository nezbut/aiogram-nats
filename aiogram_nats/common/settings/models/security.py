from dataclasses import dataclass


@dataclass
class SecretStr:

    """
    A class representing a secret string.

    Attributes :
        value (str): The secret string value.
    """

    value: str

    def __str__(self) -> str:
        """
        A method that returns a string representation of the SecretStr object.

        It replaces the actual secret string value with asterisks (*) to conceal it.

        Returns :
            str: A string representation of the SecretStr object with the secret value concealed.
        """
        return f"SecretValue({'*' * len(self.value)})"

    def __repr__(self) -> str:
        """
        A method that returns a string representation of the object.

        It is equivalent to the __str__ method and returns the same string.

        Returns :
            str: A string representation of the object.
        """
        return self.__str__()
