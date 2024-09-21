from collections.abc import Iterable
from pathlib import Path
from typing import Optional

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub
from fluentogram.src.abc import AbstractTranslator

from aiogram_nats.tgbot.i18n.enums import CountryLocale, LanguageLocale


def get_translator_hub(
        root_locale: str = "en",
        separator: str = "-",
) -> TranslatorHub:
    """
    Creates a TranslatorHub instance with the given root locale and separator.

    :param root_locale: str: The root locale for the TranslatorHub. Defaults to "en".
    :param separator: str: The separator used to join locales. Defaults to "-".

    :return: (TranslatorHub): The created TranslatorHub instance.
    """
    locales_map = _get_locales_map()
    translators = _get_translators()

    return TranslatorHub(
        locales_map=locales_map,
        translators=translators,
        root_locale=root_locale,
        separator=separator,
    )


def _get_locales_map() -> dict[str, Iterable[str]]:
    locales_map: dict[str, Iterable[str]] = {}
    for locale in LanguageLocale:
        locales = list(LanguageLocale)
        locales.remove(locale)
        locales.insert(0, locale)
        locales_map[locale.value] = tuple(loc.value for loc in locales)
    return locales_map


def _get_translators(separator: str = "-") -> list[AbstractTranslator]:
    translators: list[AbstractTranslator] = []
    for lang_locale, country_locale in zip(LanguageLocale, CountryLocale, strict=False):
        ftl_files = _parse_ftl_files_by_locale(lang_locale)
        translator = FluentTranslator(
            locale=lang_locale.value,
            translator=FluentBundle.from_files(
                locale=country_locale.value,
                filenames=ftl_files,
            ),
            separator=separator,
        )
        translators.append(translator)
    return translators


def _parse_ftl_files_by_locale(locale: LanguageLocale, locales_dir: Optional[Path] = None) -> list[str]:
    _locales_dir = locales_dir or Path(
        __file__).parent / "locales" / locale.value
    return [str(path) for path in _locales_dir.rglob("*.ftl")]
