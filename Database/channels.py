from datetime import datetime

from .connection import db


class ChannelDB:

    def __init__(self):
        self.col = db.channels

    async def add_channel(
        self,
        channel_id: int,
        title: str,
        username: str,
        short_code: str,
        added_by: int,
    ):

        data = {
            "channel_id": channel_id,
            "title": title,
            "username": username,
            "short_code": short_code,

            # Request Settings
            "auto_accept": True,
            "expire_time": 60,

            # Approved DM
            "welcome_text":
                "🎉 Your join request has been approved!\n\n"
                "Enjoy watching ❤️",

            "welcome_photo": None,

            "welcome_buttons": [],

            # Status
            "enabled": True,

            # Meta
            "added_by": added_by,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        await self.col.update_one(
            {
                "channel_id": channel_id
            },
            {
                "$set": data
            },
            upsert=True,
        )

    async def get_channel(
        self,
        channel_id: int,
    ):

        return await self.col.find_one(
            {
                "channel_id": channel_id
            }
        )

    async def get_by_short_code(
        self,
        code: str,
    ):

        return await self.col.find_one(
            {
                "short_code": code.upper()
            }
        )

    async def remove_channel(
        self,
        channel_id: int,
    ):

        return await self.col.delete_one(
            {
                "channel_id": channel_id
            }
        )

    async def channel_exists(
        self,
        channel_id: int,
    ):

        return (
            await self.col.count_documents(
                {
                    "channel_id": channel_id
                },
                limit=1,
            )
        ) > 0

    async def total_channels(self):

        return await self.col.count_documents({})

    async def get_channels(
        self,
        page=1,
        limit=10,
    ):

        skip = (page - 1) * limit

        data = []

        cursor = (
            self.col.find({})
            .sort("title", 1)
            .skip(skip)
            .limit(limit)
        )

        async for i in cursor:
            data.append(i)

        return data

    async def set_auto_accept(
        self,
        channel_id,
        status,
    ):

        await self.col.update_one(
            {
                "channel_id": channel_id
            },
            {
                "$set": {
                    "auto_accept": status,
                    "updated_at": datetime.utcnow(),
                }
            }
        )

    async def set_expire_time(
        self,
        channel_id,
        seconds,
    ):

        await self.col.update_one(
            {
                "channel_id": channel_id
            },
            {
                "$set": {
                    "expire_time": seconds,
                    "updated_at": datetime.utcnow(),
                }
            }
        )

    async def set_welcome_text(
        self,
        channel_id,
        text,
    ):

        await self.col.update_one(
            {
                "channel_id": channel_id
            },
            {
                "$set": {
                    "welcome_text": text,
                    "updated_at": datetime.utcnow(),
                }
            }
        )

    async def set_welcome_photo(
        self,
        channel_id,
        file_id,
    ):

        await self.col.update_one(
            {
                "channel_id": channel_id
            },
            {
                "$set": {
                    "welcome_photo": file_id,
                    "updated_at": datetime.utcnow(),
                }
            }
        )

    async def set_buttons(
        self,
        channel_id,
        buttons,
    ):

        await self.col.update_one(
            {
                "channel_id": channel_id
            },
            {
                "$set": {
                    "welcome_buttons": buttons,
                    "updated_at": datetime.utcnow(),
                }
            }
        )


channels_db = ChannelDB()
