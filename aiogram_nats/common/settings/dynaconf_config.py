from dynaconf import Dynaconf  # type: ignore[import-untyped]


def _lowercase_keys(d: dict) -> dict:
    if isinstance(d, dict):
        return {k.lower(): _lowercase_keys(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [_lowercase_keys(i) for i in d]
    else:
        return d


_dyna = Dynaconf(envvar_prefix="AIOGRAM_NATS")
dynaconf_settings = _lowercase_keys(_dyna.as_dict())
