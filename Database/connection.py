from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from config import MONGO_URI, DATABASE_NAME


class Database:

    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.database = self.client[DATABASE_NAME]

        self.users = self.database.users
        self.channels = self.database.channels
        self.links = self.database.links
        self.settings = self.database.settings
        self.admins = self.database.admins
        self.owners = self.database.owners
        self.logs = self.database.logs

    async def ping(self):
        await self.client.admin.command("ping")

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


db = Database()
