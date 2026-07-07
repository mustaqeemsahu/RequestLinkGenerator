from datetime import datetime

from .connection import db


class ChannelDB:

    def __init__(self):
        self.col = db.channels

    async def add_channel(
        self,
        channel_id: int,
        title: str,
        username: str = None,
        short_code: str = None,
        added_by: int = None,
    ):

        channel = await self.col.find_one(
            {"channel_id": channel_id}
        )

        data = {
            "channel_id": channel_id,
            "title": title,
            "username": username,
            "short_code": short_code,
            "added_by": added_by,
            "updated_at": datetime.utcnow(),
        }

        if channel:

            await self.col.update_one(
                {"channel_id": channel_id},
                {"$set": data},
            )

            return False

        data["created_at"] = datetime.utcnow()

        await self.col.insert_one(data)

        return True

    async def get_channel(
        self,
        channel_id: int,
    ):

        return await self.col.find_one(
            {"channel_id": channel_id}
        )

    async def get_channel_by_code(
        self,
        short_code: str,
    ):

        return await self.col.find_one(
            {"short_code": short_code}
        )

    async def remove_channel(
        self,
        channel_id: int,
    ):

        return await self.col.delete_one(
            {"channel_id": channel_id}
        )

    async def total_channels(self):

        return await self.col.count_documents({})

    async def channel_exists(
        self,
        channel_id: int,
    ):

        return (
            await self.col.count_documents(
                {"channel_id": channel_id},
                limit=1,
            )
        ) > 0

    async def get_all_channels(self):

        channels = []

        async for channel in self.col.find():
            channels.append(channel)

        return channels

    async def update_short_code(
        self,
        channel_id: int,
        short_code: str,
    ):

        await self.col.update_one(
            {"channel_id": channel_id},
            {
                "$set": {
                    "short_code": short_code,
                    "updated_at": datetime.utcnow(),
                }
            }
        )


channels_db = ChannelDB()
