from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from aiogram_nats.common.settings.models.db import RDBSettings
from aiogram_nats.infrastructure.database.rdb.factory import create_engine, create_session_maker
from aiogram_nats.infrastructure.database.rdb.holder import HolderDAO
from aiogram_nats.infrastructure.database.rdb.tm import TransactionManager


class DbProvider(Provider):

    """Provider for database"""

    scope = Scope.APP

    @provide
    async def get_engine(self, rdb_settings: RDBSettings) -> AsyncIterable[AsyncEngine]:
        """Provides an asynchronous database engine based on the provided configuration."""
        engine = create_engine(rdb_settings)
        yield engine
        await engine.dispose(close=True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        """Creates a session maker for the given asynchronous database engine."""
        return create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        """Provides an asynchronous database session based on the given session maker."""
        async with pool() as session:
            yield session


class TMProvider(Provider):

    """Provider for Transaction Manager"""

    @provide(scope=Scope.REQUEST)
    async def get_tm(self, session: AsyncSession) -> AsyncIterable[TransactionManager]:
        """Provides a Transaction Manager instance for the given asynchronous database session."""
        async with TransactionManager(session) as tm:
            yield tm


class DAOProvider(Provider):

    """Provider for DAO objects."""

    holder = provide(HolderDAO, scope=Scope.REQUEST)


def get_database_providers() -> list[Provider]:
    """Returns a list of database providers for di."""
    return [
        DbProvider(),
        TMProvider(),
        DAOProvider(),
    ]
