from aiogram_nats.infrastructure.database.rdb.dao.user import UserDAO
from aiogram_nats.infrastructure.database.rdb.tm import TransactionManager


class HolderDAO:

    """
    A container class that holds all DAO objects and provides a convenient way to commit transactions.

    DAO :
        user (UserDAO): The user DAO instance.

    Methods :
        commit: Commits the current transaction.
    """

    def __init__(self, manager: TransactionManager) -> None:
        self._manager = manager
        self.user = UserDAO(self._manager.session)

    async def commit(self) -> None:
        """Commits the current transaction."""
        await self._manager.commit()
