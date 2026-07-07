from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)

from database import channels_db
from utils.permissions import permissions
from utils.shortlink import shortlink

CHANNELS_PER_PAGE = 10


async def add_channel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user = update.effective_user

    if not await permissions.is_admin(user.id):

        return await update.message.reply_text(
            "❌ You are not allowed to use this command."
        )

    if len(context.args) != 1:

        return await update.message.reply_text(
            "Usage:\n"
            "/addchannel <Channel ID | @username>"
        )

    target = context.args[0]

    try:

        chat = await context.bot.get_chat(target)

    except Exception:

        return await update.message.reply_text(
            "❌ Invalid Channel."
        )

    try:

        me = await context.bot.get_chat_member(
            chat.id,
            context.bot.id,
        )

    except Exception:

        return await update.message.reply_text(
            "❌ Add me as admin first."
        )

    if me.status != "administrator":

        return await update.message.reply_text(
            "❌ Add me as administrator first."
        )

    exists = await channels_db.channel_exists(
        chat.id
    )

    if exists:

        return await update.message.reply_text(
            "⚠️ Channel already exists."
        )

    code = await shortlink.generate(
        username=chat.username,
        title=chat.title,
    )

    await channels_db.add_channel(
        channel_id=chat.id,
        title=chat.title,
        username=chat.username,
        short_code=code,
        added_by=user.id,
    )

    text = (
        "✅ Channel Added Successfully\n\n"
        f"📺 Name : {chat.title}\n"
        f"🆔 ID : <code>{chat.id}</code>\n"
        f"👤 Username : @{chat.username if chat.username else 'Private'}\n"
        f"🔗 Code : <code>{code}</code>"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
    )


add_channel_handler = CommandHandler(
    "addchannel",
    add_channel,
  )

async def remove_channel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user = update.effective_user

    if not await permissions.is_admin(user.id):
        return await update.message.reply_text(
            "❌ You are not allowed to use this command."
        )

    if len(context.args) != 1:
        return await update.message.reply_text(
            "Usage:\n/removechannel <Channel ID>"
        )

    try:
        channel_id = int(context.args[0])
    except ValueError:
        return await update.message.reply_text(
            "❌ Invalid Channel ID."
        )

    channel = await channels_db.get_channel(channel_id)

    if not channel:
        return await update.message.reply_text(
            "❌ Channel not found."
        )

    await channels_db.remove_channel(channel_id)

    await update.message.reply_text(
        f"✅ Removed **{channel['title']}** successfully.",
        parse_mode="Markdown"
    )


async def channels(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    page = 1

    channels = await channels_db.get_channels_page(
        page,
        10,
    )

    total = await channels_db.total_channels()

    pages = (total + 9) // 10

    text = "<b>📺 Channels</b>\n\n"

    for i, ch in enumerate(channels, start=1):

        text += (
            f"{i}. <b>{ch['title']}</b>\n"
            f"<code>{ch['channel_id']}</code>\n"
            f"🔗 {ch['short_code']}\n\n"
        )

    keyboard = []

    if pages > 1:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "Next ➡️",
                    callback_data="channels_2",
                )
            ]
        )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def get_channels_page(
        self,
        page: int = 1,
        limit: int = 10,
    ):

        skip = (page - 1) * limit

        channels = []

        cursor = (
            self.col
            .find({})
            .sort("created_at", 1)
            .skip(skip)
            .limit(limit)
        )

        async for channel in cursor:
            channels.append(channel)

        return channels

    async def search_channel(
        self,
        keyword: str,
    ):

        return await self.col.find_one(
            {
                "$or": [
                    {
                        "title": {
                            "$regex": keyword,
                            "$options": "i",
                        }
                    },
                    {
                        "short_code": {
                            "$regex": keyword,
                            "$options": "i",
                        }
                    },
                    {
                        "username": {
                            "$regex": keyword,
                            "$options": "i",
                        }
                    },
                ]
            }
    )
