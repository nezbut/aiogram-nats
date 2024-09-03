from abc import ABC, abstractmethod
from typing import Any


class AbstractTranslator(ABC):

    @abstractmethod
    def __init__(self, locale: str, translator: Any,
                 separator: str = "-") -> None: ...

    @abstractmethod
    def get(self, key: str, **kwargs: Any) -> str: ...
