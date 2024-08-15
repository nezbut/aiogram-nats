import logging

from structlog.typing import EventDict


def logger_detailed(logger: logging.Logger, method_name: str, event_dict: EventDict) -> EventDict:
    """

    A processor function for structlog that extracts filename, function name, and line number from an event dictionary.

    It takes a logger, method name, and an event dictionary as input, extracts the filename, function name, and line number,
    and adds them to the event dictionary in the format "filename:function_name:line_number".

    Args :
        logger (logging.Logger): The logger instance.
        method_name (str): The name of the method.
        event_dict (EventDict): The event dictionary.

    Returns :
        EventDict: The updated event dictionary.
    """
    filename: str = event_dict.pop("filename")
    func_name: str = event_dict.pop("func_name")
    lineno: str = event_dict.pop("lineno")

    event_dict["logger"] = f"{filename}:{func_name}:{lineno}"

    return event_dict
