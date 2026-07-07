from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)

from database import channels_db
from utils.permissions import permissions
from utils.shortlink import shortlink


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
