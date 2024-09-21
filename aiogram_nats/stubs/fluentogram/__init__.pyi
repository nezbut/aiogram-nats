from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:  # noqa: PYI002
    from fluent_compiler.bundle import FluentBundle

    from .src.abc import AbstractTranslator


class FluentTranslator(AbstractTranslator):

    def __init__(self, locale: str, translator: FluentBundle,
                 separator: str = "-"): ...

    def get(self, key: str, **kwargs: Any) -> str: ...


class TranslatorHub:

    def __init__(
            self,
            locales_map: dict[str, Union[str, Iterable[str]]],
            translators: list[AbstractTranslator],
            root_locale: str = "en",
            separator: str = "-",
    ) -> None: ...

    def get_translator_by_locale(self, locale: str) -> TranslatorRunner: ...


class TranslatorRunner:

    def __init__(
            self, translators: Iterable[AbstractTranslator], separator: str = "-") -> None: ...

    def get(self, key: str, **kwargs: Any) -> str: ...

    def __call__(self, **kwargs: Any) -> str: ...

    def __getattr__(self, item: str) -> TranslatorRunner: ...
