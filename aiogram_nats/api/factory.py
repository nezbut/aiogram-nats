from asgi_monitor.integrations.fastapi import MetricsConfig, setup_metrics
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from structlog.stdlib import BoundLogger

from aiogram_nats.api import middlewares


def create_app(container: AsyncContainer, logger: BoundLogger) -> FastAPI:
    """Create FastAPI app"""
    app = FastAPI()
    setup_dishka(container, app)
    middlewares.setup(app, logger)
    setup_metrics(
        app,
        MetricsConfig(
            app_name="aiogram_nats",
            include_metrics_endpoint=True,
            include_trace_exemplar=True,
        ),
    )
    return app
