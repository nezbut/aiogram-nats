from collections.abc import Iterable

from adaptix.conversion import get_converter
from dishka import Provider, Scope, provide

from aiogram_nats.common.log.configuration import LoggerName, LoggerReg
from aiogram_nats.common.log.installer import LoggersInstaller
from aiogram_nats.common.settings.models.logs import LoggerSettings, LoggingSettings


class LoggingProvider(Provider):

    """Provider for interactors"""

    scope = Scope.APP

    @provide
    def get_installer(self, settings: LoggingSettings) -> Iterable[LoggersInstaller]:
        """Install logging"""
        convert_to_reg = get_converter(LoggerSettings, LoggerReg)
        loggers = [
            convert_to_reg(logger)
            for logger in settings.loggers
            if logger.name in LoggerName
        ]
        default_loggers = [
            LoggerReg(name=name)
            for name in LoggerName
            if name.value not in loggers
        ]

        loggers.extend(default_loggers)
        installer = LoggersInstaller(
            loggers=loggers,
            dev=settings.dev,
            log_to_file=settings.logs_to_file,
            delete_log_file=settings.delete_log_file,
            logs_dir=settings.logs_dir,
            file_write_format=settings.file_write_format,
        )
        installer.install()
        yield installer
        installer.close()


def get_logging_providers() -> list[Provider]:
    """Returns a list of logging providers for di."""
    return [LoggingProvider()]
