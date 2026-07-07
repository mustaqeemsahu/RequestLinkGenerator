from datetime import datetime, timedelta

from .connection import db


class LinkDB:

    def __init__(self):
        self.col = db.links

    async def create_link(
        self,
        code: str,
        channel_id: int,
        created_by: int,
        expire_seconds: int = 60,
    ):

        now = datetime.utcnow()

        data = {
            "code": code,
            "channel_id": channel_id,
            "created_by": created_by,
            "created_at": now,
            "expires_at": now + timedelta(seconds=expire_seconds),
            "used": False,
        }

        await self.col.insert_one(data)

        return data

    async def get_link(
        self,
        code: str,
    ):

        return await self.col.find_one(
            {
                "code": code
            }
        )

    async def link_exists(
        self,
        code: str,
    ):

        return (
            await self.col.count_documents(
                {"code": code},
                limit=1,
            )
        ) > 0

    async def is_expired(
        self,
        code: str,
    ):

        link = await self.get_link(code)

        if not link:
            return True

        return datetime.utcnow() >= link["expires_at"]

    async def mark_used(
        self,
        code: str,
    ):

        await self.col.update_one(
            {
                "code": code
            },
            {
                "$set": {
                    "used": True
                }
            }
        )

    async def delete_link(
        self,
        code: str,
    ):

        await self.col.delete_one(
            {
                "code": code
            }
        )

    async def delete_expired_links(self):

        result = await self.col.delete_many(
            {
                "expires_at": {
                    "$lt": datetime.utcnow()
                }
            }
        )

        return result.deleted_count

    async def total_links(self):

        return await self.col.count_documents({})

    async def active_links(self):

        return await self.col.count_documents(
            {
                "expires_at": {
                    "$gt": datetime.utcnow()
                }
            }
        )

    async def used_links(self):

        return await self.col.count_documents(
            {
                "used": True
            }
        )

    async def expired_links(self):

        return await self.col.count_documents(
            {
                "expires_at": {
                    "$lt": datetime.utcnow()
                }
            }
        )


links_db = LinkDB()
