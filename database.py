from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from config import MONGO_URI, DATABASE_NAME


class Database:

    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]

        self.users = self.db.users
        self.owners = self.db.owners
        self.admins = self.db.admins
        self.channels = self.db.channels
        self.links = self.db.links
        self.settings = self.db.settings
        self.logs = self.db.logs

    async def create_indexes(self):
        await self.users.create_index(
            [("user_id", ASCENDING)],
            unique=True
        )

        await self.channels.create_index(
            [("channel_id", ASCENDING)],
            unique=True
        )

        await self.links.create_index(
            [("code", ASCENDING)],
            unique=True
        )

        await self.links.create_index(
            [("expires_at", ASCENDING)]
        )

        await self.admins.create_index(
            [("user_id", ASCENDING)],
            unique=True
        )

        await self.owners.create_index(
            [("user_id", ASCENDING)],
            unique=True
        )

    async def ping(self):
        await self.client.admin.command("ping")


db = Database()
