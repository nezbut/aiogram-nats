from collections.abc import Callable, Sequence
from typing import Any, Optional


class FluentBundle:

    def __init__(self, locale: str, resources: list, functions: Optional[Callable[[Any], Any]] = None,
                 use_isolating: bool = True, escapers: Any = None) -> None: ...

    @classmethod
    def from_string(cls, locale: str, text: str, functions: Optional[Callable[[Any], Any]] = None,
                    use_isolating: bool = True, escapers: Any = None) -> FluentBundle: ...

    @classmethod
    def from_files(cls, locale: str, filenames: Sequence[str], functions: Optional[Callable[[Any], Any]] = None,
                   use_isolating: bool = True, escapers: Any = None) -> FluentBundle: ...

    def has_message(self, message_id: str) -> bool: ...

    def format(self, message_id: str, args: Any = None) -> tuple: ...

    def check_messages(self) -> list: ...
