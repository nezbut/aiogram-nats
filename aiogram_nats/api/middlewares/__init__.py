from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.stdlib import BoundLogger

from aiogram_nats.api.middlewares.log import LoggingMiddleware


def setup(app: FastAPI, logger: BoundLogger) -> None:
    """Setup api middlewares"""
    app.add_middleware(BaseHTTPMiddleware, dispatch=LoggingMiddleware(logger))
