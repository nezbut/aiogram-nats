import asyncio
from abc import ABC, abstractmethod
from typing import Any, Optional

from aiogram import Bot, Dispatcher
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, FastAPI, Request, Response
from structlog.stdlib import BoundLogger


class BaseRequestHandler(ABC):

    """Base webhook request handler."""

    def __init__(
        self,
        logger: BoundLogger,
        handle_in_background: Optional[bool] = None,
        **data: Any,
    ) -> None:
        self.handle_in_background = False if handle_in_background is None else handle_in_background
        self.data = data
        self.logger = logger
        self._background_feed_update_tasks: set[asyncio.Task[Any]] = set()

    def register(self, app: FastAPI, /, path: str, **kwargs: Any) -> None:
        """
        Registers a webhook request handler with a FastAPI application.

        :param app: FastAPI application
        :param path: path to register
        :param kwargs: additional parameters
        """
        router = APIRouter()
        router.add_api_route(
            methods=["POST"], path=path, endpoint=self.handle, **kwargs,
        )
        app.include_router(router)

    @abstractmethod
    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        """
        An abstract method that verifies the secret token of a Telegram webhook.

        :param telegram_secret_token: The secret token provided by Telegram.
        :type telegram_secret_token: str
        :param bot: The Bot instance associated with the webhook.
        :type bot: Bot
        :return: True if the secret token is valid, False otherwise.
        :rtype: bool
        """
        pass

    async def _background_feed_update(
        self,
        bot: Bot,
        dispatcher: Dispatcher,
        update: dict[str, Any],
    ) -> None:
        result = await dispatcher.feed_raw_update(bot=bot, update=update, **self.data)
        if isinstance(result, TelegramMethod):
            await dispatcher.silent_call_request(bot=bot, result=result)

    async def _handle_request_background(
        self,
        bot: Bot,
        dispatcher: Dispatcher,
        request: Request,
    ) -> Response:
        feed_update_task = asyncio.create_task(
            self._background_feed_update(
                bot=bot,
                dispatcher=dispatcher,
                update=bot.session.json_loads(request.body),
            ),
        )
        self._background_feed_update_tasks.add(feed_update_task)
        feed_update_task.add_done_callback(
            self._background_feed_update_tasks.discard)
        return Response(content={})

    async def _build_response_writer(
        self,
        bot: Bot,
        dispatcher: Dispatcher,
        result: Optional[TelegramMethod[TelegramType]],
    ) -> Any:
        if result:
            await dispatcher.silent_call_request(bot, result)

    async def _handle_request(
        self,
        bot: Bot,
        dispatcher: Dispatcher,
        request: Request,
    ) -> Response:
        result: Optional[TelegramMethod[Any]] = await dispatcher.feed_webhook_update(
            bot,
            await request.json(),
            **self.data,
        )
        return Response(
            content=await self._build_response_writer(
                bot=bot,
                dispatcher=dispatcher,
                result=result,
            ),
        )

    @inject
    async def handle(
        self,
        request: Request,
        bot: FromDishka[Bot],
        dispatcher: FromDishka[Dispatcher],
    ) -> Response:
        """
        Handles a webhook request.

        This function verifies the secret token of a Telegram webhook by calling the `verify_secret` method.
        If the token is valid, it either handles the request in the background or synchronously, depending on the value of `handle_in_background`.

        :param request: The incoming request object.
        :type request: Request
        :param bot: The Bot instance associated with the webhook.
        :type bot: Bot
        :param dispatcher: The Dispatcher instance used to feed webhook updates.
        :type dispatcher: Dispatcher
        :return: The response object.
        :rtype: Response
        """
        if not self.verify_secret(request.headers.get("X-Telegram-Bot-Api-Secret-Token", ""), bot):
            return Response(content="Unauthorized", status_code=401)
        if self.handle_in_background:
            return await self._handle_request_background(
                bot=bot, dispatcher=dispatcher, request=request,
            )
        return await self._handle_request(bot=bot, dispatcher=dispatcher, request=request)

    __call__ = handle
