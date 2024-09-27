import logging.config
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import structlog
from structlog.typing import Processor

from aiogram_nats.common.log.configuration import Formatter, Handler, LoggerName, LoggerReg
from aiogram_nats.common.log.processors.detailed import logger_detailed


class _LogFileState(Enum):
    CURRENT = "(CURRENT)"
    OLD = "(OLD)"


class LoggersInstaller:

    """
    A class responsible for installing loggers.

    This class takes care of setting up loggers with the specified configuration.
    It provides methods for installing and closing loggers.

    Attributes :
        loggers (list[LoggerReg]): A list of loggers to be installed.
        dev (bool): A flag indicating whether to use development mode.
        log_to_file (bool): A flag indicating whether to log to a file.
        delete_log_file (bool): A flag indicating whether to delete the log file.
        logs_dir (str): The directory where log files are stored.
        file_write_format (Formatter): The format used for writing logs to a file.

    """

    def __init__(
            self,
            loggers: list[LoggerReg],
            *,
            dev: bool = False,
            log_to_file: bool = False,
            delete_log_file: bool = True,
            logs_dir: str = "logs",
            file_write_format: Formatter = Formatter.JSON,
    ) -> None:
        self.loggers = loggers
        self.dev = dev
        self.log_to_file = log_to_file
        self.logs_dir = Path(logs_dir)
        self.file_write_format = file_write_format.value
        self._delete_log_file = delete_log_file
        self._log_file: Optional[Path] = None

    def __str__(self) -> str:
        """
        Returns a string representation of the LoggersInstaller object.

        The string includes the class name, development mode status, and the number of registered loggers.
        """
        return f"<{self.__class__.__name__} dev:{self.dev}; Reg {len(self.loggers)} loggers>"

    def __enter__(self) -> None:
        """
        Enter the runtime context.

        This method is called when the object is used in a `with` statement.
        It installs the loggers.
        """
        self.install()

    def __exit__(self, *args: object) -> None:
        """
        Exit the runtime context.

        This method is called when the object is used in a `with` statement.
        It closes the loggers.

        Parameters :
            *args (object): The arguments passed to the `__exit__` method.
        """
        self.close()

    @property
    def _renderer(self) -> str:
        handler = Handler.CONSOLE if self.dev else Handler.JSON
        return handler.value

    @property
    def _timestamper(self) -> structlog.processors.TimeStamper:
        return structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")

    def _preprocessors(self, *, additional: bool = False) -> list[Processor]:
        preprocessors: list[Processor] = [
            self._timestamper,
            structlog.stdlib.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                },
            ),
            logger_detailed,
        ]
        if additional:
            additional_preprocessors: list[Processor] = [
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.filter_by_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ]
            preprocessors.extend(additional_preprocessors)
        return preprocessors

    def install(self) -> None:
        """
        Installs the loggers with the specified configuration.

        This method sets up the loggers with the provided configuration, including the log level, handlers, and formatters.
        It also configures the structlog library to use the specified processors and logger factory.

        """
        handlers = {
            Handler.CONSOLE.value: {
                "class": "logging.StreamHandler",
                "formatter": Formatter.CONSOLE.value,
            },
            Handler.JSON.value: {
                "class": "logging.StreamHandler",
                "formatter": Formatter.JSON.value,
            },
        }

        if self.log_to_file:
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            date = datetime.now(UTC).strftime("%d.%m.%Y_%H_%M_%S")
            log_filename = f"{self.logs_dir}/{date}{_LogFileState.CURRENT.value if not self._delete_log_file else ''}.log"
            self._log_file = Path(log_filename)

            file_handler = {
                "class": "logging.FileHandler",
                "filename": log_filename,
                "formatter": self.file_write_format,
            }
            handlers["file_handler"] = file_handler

        logging.config.dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    Formatter.JSON.value: {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.processors.JSONRenderer(),
                        "foreign_pre_chain": self._preprocessors(),
                    },
                    Formatter.CONSOLE.value: {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.dev.ConsoleRenderer(),
                        "foreign_pre_chain": self._preprocessors(),
                    },
                },
                "handlers": handlers,
                "loggers": {
                    f"{log.name.value}": {
                        "handlers": [self._renderer, "file_handler"] if log.write_file and self.log_to_file else [
                            self._renderer],
                        "level": log.level.value,
                        "propagate": log.propagate,
                    }
                    for log in self.loggers
                },
            },
        )

        structlog.configure(
            processors=self._preprocessors(additional=True),
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def close(self) -> None:
        """
        Closes the loggers and performs necessary cleanup operations.

        This method shuts down the logging system, and if log_to_file is True, it deletes or renames the log file based on the _delete_log_file flag.

        """
        logging.shutdown()
        if not self.log_to_file:
            return

        if not isinstance(self._log_file, Path):
            raise TypeError("Log file was not created")

        if self._delete_log_file:
            self._log_file.unlink(missing_ok=True)
        elif not self._delete_log_file and self.log_to_file:
            new_name = self._log_file.parent / \
                f"{self._log_file.name[:-(len(_LogFileState.CURRENT.value) + 4)]}{_LogFileState.OLD.value}.log"
            self._log_file.rename(new_name)

    def get_logger(self, name: LoggerName, **constant_data: Any) -> structlog.stdlib.BoundLogger:
        """Returns a structlog BoundLogger instance for the specified logger name."""
        return structlog.stdlib.get_logger(name.value, **constant_data)
