from dataclasses import dataclass
from enum import Enum


class Level(Enum):

    """
    An enumeration of log levels.

    The log levels are used to categorize log messages by their severity.
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Handler(Enum):

    """
    An enumeration of log handlers.

    The log handlers are used to determine the destination of log messages.
    """

    CONSOLE = "console"
    JSON = "jsonformat"


class Formatter(Enum):

    """
    An enumeration of log formatters.

    The log formatters are used to determine the format of log messages.
    """

    CONSOLE = "console_formatter"
    JSON = "jsonformat_formatter"


class LoggerName(Enum):

    """
    An enumeration of logger names.

    The logger names are used to identify different loggers in the application.
    """

    SCHEDULER = "scheduler"
    AIOGRAM_BOT = "aiogram_bot"
    MAILING = "mailing"
    SCHEDULE_MESSAGE = "schedule_message"
    USER = "user"


@dataclass
class LoggerReg:

    """
    Represents a logger registration.

    Attributes :
        name (LoggerName): The name of the logger.
        level (Level): The log level of the logger. Defaults to Level.DEBUG.
        propagate (bool): Whether to propagate log messages to parent loggers. Defaults to False.
        write_file (bool): Whether to write log messages to a file. Defaults to False.
    """

    name: LoggerName
    level: Level = Level.DEBUG
    propagate: bool = False
    write_file: bool = False
