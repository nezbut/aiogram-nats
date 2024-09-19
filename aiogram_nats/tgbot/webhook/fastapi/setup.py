from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from aiogram import Dispatcher
from dishka import AsyncContainer
from fastapi import APIRouter, FastAPI


def setup_application(app: FastAPI, container: AsyncContainer, /, **kwargs: Any) -> None:
    """Setup webhook application."""
    workflow_data = {
        "app": app,
        "container": container,
        **kwargs,
    }

    @asynccontextmanager
    async def lifespan(*a: Any, **kw: Any) -> AsyncIterator[None]:
        dispatcher = await container.get(Dispatcher)
        await dispatcher.emit_startup(**workflow_data, **dispatcher.workflow_data)
        yield
        await dispatcher.emit_shutdown(**workflow_data, **dispatcher.workflow_data)

    app.include_router(APIRouter(lifespan=lifespan))
