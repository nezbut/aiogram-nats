from dynaconf import Dynaconf  # type: ignore[import-untyped]

dynaconf_settings = Dynaconf(envvar_prefix="AIOGRAM_NATS")
