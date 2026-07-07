from datetime import datetime

from .connection import db


class SettingsDB:

    def __init__(self):
        self.col = db.settings

    async def get(self):

        settings = await self.col.find_one({"_id": "BOT_SETTINGS"})

        if settings:
            return settings

        default = {
            "_id": "BOT_SETTINGS",

            "start_text":
                "👋 Hello {first_name}!\n\n"
                "Welcome to {bot_name}.",

            "start_photo": None,

            "start_buttons": [],

            "force_sub": [],

            "log_group": None,

            "link_expire": 60,

            "maintenance": False,

            "broadcast_sleep": 0.05,

            "about_text":
                "Request Manager Bot",

            "help_text":
                "Use the buttons below.",

            "updated_at": datetime.utcnow()
        }

        await self.col.insert_one(default)

        return default

    async def update(self, key, value):

        await self.col.update_one(
            {"_id": "BOT_SETTINGS"},
            {
                "$set": {
                    key: value,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )

    async def get_value(self, key):

        settings = await self.get()

        return settings.get(key)

    async def add_force_sub(self, channel_id):

        await self.col.update_one(
            {"_id": "BOT_SETTINGS"},
            {
                "$addToSet": {
                    "force_sub": channel_id
                }
            },
            upsert=True
        )

    async def remove_force_sub(self, channel_id):

        await self.col.update_one(
            {"_id": "BOT_SETTINGS"},
            {
                "$pull": {
                    "force_sub": channel_id
                }
            }
        )

    async def set_log_group(self, chat_id):

        await self.update(
            "log_group",
            chat_id
        )

    async def set_start_message(self, text):

        await self.update(
            "start_text",
            text
        )

    async def set_start_photo(self, file_id):

        await self.update(
            "start_photo",
            file_id
        )

    async def set_buttons(self, buttons):

        await self.update(
            "start_buttons",
            buttons
        )

    async def set_link_expire(self, seconds):

        await self.update(
            "link_expire",
            seconds
        )

    async def enable_maintenance(self):

        await self.update(
            "maintenance",
            True
        )

    async def disable_maintenance(self):

        await self.update(
            "maintenance",
            False
        )


settings_db = SettingsDB()
