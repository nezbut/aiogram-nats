from uuid import UUID

from adaptix import dump
from aiogram.fsm.context import FSMContext

from aiogram_nats.core.entities.mailing import Mailing, MailingMessage
from aiogram_nats.core.entities.user import User
from aiogram_nats.core.interfaces.interfaces.mailing import MailingManager
from aiogram_nats.infrastructure.clients.mailing_service import MailingServiceClient
from aiogram_nats.infrastructure.database.rdb.dao.user import UserDAO


class MailingManagerImpl(MailingManager):

    """
    A class that manages mailing operations.

    This class provides methods to create, save, and remove mailing objects.
    """

    def __init__(self, client: MailingServiceClient, context: FSMContext, user_dao: UserDAO) -> None:
        self.mailing_service = client
        self.ctx = context
        self.dao = user_dao

    async def create(self, message: MailingMessage, creator: User, users: list[User]) -> Mailing:
        """
        Asynchronously creates a new mailing.

        Args :
            message (MailingMessage): The message of the mailing.
            users (list[User]): The list of users associated with the mailing.
            creator (User): The creator of the mailing.

        Returns :
            Mailing: The newly created mailing.

        """
        users_dict = [dump(user) for user in users]
        mailing_id_str = await self.mailing_service.create_mailing(users_dict)
        mailing_id = UUID(mailing_id_str)

        return Mailing(
            id=mailing_id,
            creator=creator,
            users=users,
            message=message,
        )

    async def save(self, mailing: Mailing) -> None:
        """
        Asynchronously saves a mailing.

        Args :
            mailing (Mailing): The mailing to be saved.

        """
        db_count = await self.dao.count()
        users = "all" if len(mailing.users) == db_count else [
            user.id for user in mailing.users
        ]
        data = dump(mailing)
        data["users"] = users
        await self.ctx.update_data(mailing=data)

    async def remove(self, mailing: Mailing) -> None:
        """
        Remove a mailing from the system.

        Args :
            mailing (Mailing): The mailing object to be removed.

        """
        await self.ctx.update_data(mailing=None)
        await self.mailing_service.delete_mailing(str(mailing.id))
