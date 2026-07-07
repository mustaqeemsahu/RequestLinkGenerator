from telegram import Update
from telegram.ext import ContextTypes

from config import OWNER_ID
from database import (
    users_db,
    settings_db,
    db
)


class Permissions:

    @staticmethod
    async def is_owner(user_id: int) -> bool:

        if user_id == OWNER_ID:
            return True

        owner = await db.owners.find_one(
            {
                "user_id": user_id
            }
        )

        return owner is not None

    @staticmethod
    async def is_admin(user_id: int) -> bool:

        if await Permissions.is_owner(user_id):
            return True

        admin = await db.admins.find_one(
            {
                "user_id": user_id
            }
        )

        return admin is not None

    @staticmethod
    async def is_banned(user_id: int) -> bool:

        user = await users_db.get_user(user_id)

        if not user:
            return False

        return user.get("banned", False)

    @staticmethod
    async def in_maintenance() -> bool:

        return await settings_db.get_value(
            "maintenance"
        )

    @staticmethod
    async def check_force_sub(
        bot,
        user_id: int,
    ):

        channels = await settings_db.get_value(
            "force_sub"
        )

        if not channels:
            return True

        for channel in channels:

            try:

                member = await bot.get_chat_member(
                    channel,
                    user_id,
                )

                if member.status in (
                    "left",
                    "kicked",
                ):
                    return False

            except Exception:
                return False

        return True


permissions = Permissions()
