from collections.abc import Awaitable, Callable

from fastapi import Request, Response


class LoggingMiddleware:

    """Middleware for logging requests and responses"""

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Loggging requests and response"""
        ...
        return await call_next(request)
