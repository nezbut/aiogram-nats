from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from aiogram_nats.api.middlewares.log import LoggingMiddleware


def setup(app: FastAPI) -> None:
    """Setup api middlewares"""
    app.add_middleware(BaseHTTPMiddleware, dispatch=LoggingMiddleware())
