from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from aiogram_nats.common.settings.models.db import RDBSettings


def create_engine(settings: RDBSettings) -> AsyncEngine:
    """
    Creates an asynchronous database engine based on the provided configuration.

    Args :
        settings (RDBSettings): The relational database settings to use for engine creation.

    Returns :
        AsyncEngine: The created asynchronous database engine.
    """
    return create_async_engine(url=make_url(settings.make_uri().value), echo=settings.echo)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Creates a session maker for the given asynchronous database engine.

    Args :
        engine (AsyncEngine): The asynchronous database engine to bind the session maker to.

    Returns :
        async_sessionmaker[AsyncSession]: A session maker that creates sessions bound to the given engine.
    """
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False,
    )
    return pool
