from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from structlog.stdlib import BoundLogger


class LoggingMiddleware:

    """Middleware for logging requests and responses"""

    def __init__(self, logger: BoundLogger) -> None:
        self.logger = logger

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Loggging requests and response"""
        await self.logger.adebug("Got request. url: %s, headers: %s",
                     request.url, request.headers)
        response = await call_next(request)
        await self.logger.adebug(
            "Response will be: status: %s, headers: %s", response.status_code, response.headers,
        )
        return response
