from datetime import datetime

from .connection import db


class UserDB:

    def __init__(self):
        self.col = db.users

    async def add_user(
        self,
        user_id: int,
        first_name: str,
        username: str = None,
    ):

        user = await self.col.find_one(
            {"user_id": user_id}
        )

        data = {
            "user_id": user_id,
            "first_name": first_name,
            "username": username,
            "updated_at": datetime.utcnow(),
        }

        if user:

            await self.col.update_one(
                {"user_id": user_id},
                {"$set": data},
            )

            return False

        data.update(
            {
                "joined_at": datetime.utcnow(),
                "banned": False,
            }
        )

        await self.col.insert_one(data)

        return True

    async def get_user(self, user_id: int):

        return await self.col.find_one(
            {"user_id": user_id}
        )

    async def is_user(self, user_id: int):

        return (
            await self.col.count_documents(
                {"user_id": user_id},
                limit=1,
            )
        ) > 0

    async def total_users(self):

        return await self.col.count_documents({})

    async def ban_user(self, user_id: int):

        await self.col.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "banned": True
                }
            }
        )

    async def unban_user(self, user_id: int):

        await self.col.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "banned": False
                }
            }
        )


users_db = UserDB()
