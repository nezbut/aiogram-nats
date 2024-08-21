from types import TracebackType
from typing import Optional, Self

from sqlalchemy.ext.asyncio.session import AsyncSession


class TransactionManager:

    """
    A class that manages database transactions.

    It provides methods for committing, rolling back, and closing transactions.
    """

    def __init__(self, session: AsyncSession, *, auto_commit: bool = False) -> None:
        self.auto_commit = auto_commit
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """
        Returns the session property of the TransactionManager.

        :return: An AsyncSession object representing the session.
        :rtype: AsyncSession
        """
        return self._session

    async def commit(self) -> None:
        """Commits the current transaction."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Rolls back the current transaction."""
        await self._session.rollback()

    async def close(self) -> None:
        """Closes the current session."""
        await self._session.close()

    async def __aenter__(self) -> Self:
        """
        Asynchronous context manager entry point.

        :return: The TransactionManager instance itself.
        :rtype: Self
        """
        return self

    async def __aexit__(
            self,
            exc_type: Optional[type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        """
        Asynchronous context manager exit point.

        This method is called when exiting an asynchronous context managed by the TransactionManager instance.
        It handles any exceptions that occurred within the context and performs the necessary cleanup.

        :param exc_type: The type of exception that occurred, if any.
        :param exc_val: The value of the exception that occurred, if any.
        :param exc_tb: The traceback of the exception that occurred, if any.
        :return: None
        """
        if exc_type is not None and exc_val is not None:
            await self.rollback()
            await self.close()
            raise exc_val
        if self.auto_commit:
            await self.commit()
        await self.close()

    def __str__(self) -> str:
        """
        Returns a string representation of the TransactionManager instance.

        :return: A string containing the class name of the TransactionManager instance.
        :rtype: str
        """
        return f"{self.__class__.__name__}"
