from enum import Enum


class LanguageLocale(Enum):

    """Enum representing the supported languages."""

    RU = "ru"
    EN = "en"


class CountryLocale(Enum):

    """Enum representing the supported countries and their locales."""

    RU = "ru-RU"
    EN = "en-US"
