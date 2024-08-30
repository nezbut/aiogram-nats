from dataclasses import dataclass
from typing import Any

from aiogram_nats.common.log.configuration import Formatter, Level, LoggerName


@dataclass
class LoggerSettings:

    """
    A class representing the settings for a logger.

    Attributes :
        name (LoggerName): The name of the logger.
        level (Level): The logging level.
        propagate (bool): Whether to propagate log messages to parent loggers.
        write_file (bool): Whether to write log messages to a file.
    """

    name: LoggerName
    level: Level = Level.DEBUG
    propagate: bool = False
    write_file: bool = False


@dataclass
class LoggingSettings:

    """
    A class representing the logging settings.

    Attributes :
        dev (bool): Whether the application is in development mode.
        logs_to_file (bool): Whether to log messages to a file.
        delete_log_file (bool): Whether to delete the log file after logging.
        logs_dir (str): The directory where log files are stored.
        file_write_format (Formatter): The format used to write log messages to a file.
    """

    loggers: tuple[LoggerSettings, ...] = ()
    dev: bool = False
    logs_to_file: bool = False
    delete_log_file: bool = True
    logs_dir: str = "logs"
    file_write_format: Formatter = Formatter.JSON


def get_logging_settings() -> list[Any]:
    """Returns a list of logging settings classes."""
    return [LoggingSettings]


__all__ = ["get_logging_settings"]
