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
from utils.shortlink import shortcode


BOT_USERNAME = "YOUR_BOT_USERNAME"  # Replace after deployment


async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not await permissions.is_admin(user.id):
        return await update.message.reply_text(
            "❌ You are not allowed to use this command."
        )

    if len(context.args) != 1:
        return await update.message.reply_text(
            "Usage:\n/addchannel <Channel ID | @username>"
        )

    target = context.args[0]

    try:
        chat = await context.bot.get_chat(target)
    except Exception:
        return await update.message.reply_text(
            "❌ Invalid channel."
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

    if me.status not in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ):
        return await update.message.reply_text(
            "❌ I must be an administrator."
        )

    if await channels_db.channel_exists(chat.id):
        return await update.message.reply_text(
            "⚠️ Channel already exists."
        )

    code = await shortcode.generate(
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

    deep_link = f"https://t.me/{BOT_USERNAME}?start=req_{code}"

    text = (
        "✅ <b>Channel Added Successfully</b>\n\n"
        f"📺 <b>{chat.title}</b>\n"
        f"🆔 <code>{chat.id}</code>\n"
        f"🔑 <code>{code}</code>\n\n"
        "Share Link:\n"
        f"<code>{deep_link}</code>"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔗 Open Link",
                    url=deep_link,
                )
            ]
        ]
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not await permissions.is_admin(user.id):
        return await update.message.reply_text("❌ Permission denied.")

    if len(context.args) != 1:
        return await update.message.reply_text(
            "/removechannel <Channel ID>"
        )

    try:
        channel_id = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("❌ Invalid Channel ID.")

    if not await channels_db.channel_exists(channel_id):
        return await update.message.reply_text("❌ Channel not found.")

    await channels_db.remove_channel(channel_id)

    await update.message.reply_text(
        "✅ Channel removed successfully."
    )


async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await permissions.is_admin(update.effective_user.id):
        return

    channels = await channels_db.get_channels(page=1, limit=10)

    if not channels:
        return await update.message.reply_text("No channels added.")

    text = "<b>📺 Channels</b>\n\n"

    for i, ch in enumerate(channels, start=1):
        text += (
            f"{i}. <b>{ch['title']}</b>\n"
            f"🔑 <code>{ch['short_code']}</code>\n"
            f"🆔 <code>{ch['channel_id']}</code>\n\n"
        )

    total = await channels_db.total_channels()

    text += f"Total : <b>{total}</b>"

    await update.message.reply_text(
        text,
        parse_mode="HTML",
    )


add_channel_handler = CommandHandler("addchannel", add_channel)
remove_channel_handler = CommandHandler("removechannel", remove_channel)
channels_handler = CommandHandler("channels", channels)
