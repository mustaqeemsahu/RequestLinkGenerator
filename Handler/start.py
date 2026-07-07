from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    CommandHandler,
    ContextTypes,
)

from database import (
    users_db,
    settings_db,
)

from utils.permissions import permissions
from utils.helper import join_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    bot = context.bot

    await users_db.add_user(
        user.id,
        user.first_name,
        user.username,
    )

    # Maintenance Mode

    if await permissions.in_maintenance():

        if not await permissions.is_admin(user.id):

            return await update.message.reply_text(
                "🛠 Bot is currently under maintenance.\n\nPlease try again later."
            )

    # Ban Check

    if await permissions.is_banned(user.id):

        return await update.message.reply_text(
            "🚫 You are banned from using this bot."
        )

    # Force Subscribe

    joined = await permissions.check_force_sub(
        bot,
        user.id,
    )

    if not joined:

        settings = await settings_db.get()

        channels = []

        for channel_id in settings["force_sub"]:

            try:

                chat = await bot.get_chat(channel_id)

                if chat.username:

                    link = f"https://t.me/{chat.username}"

                else:

                    invite = await bot.create_chat_invite_link(
                        chat.id
                    )

                    link = invite.invite_link

                channels.append(
                    (
                        chat.title,
                        link,
                    )
                )

            except Exception:

                continue

        return await update.message.reply_text(
            "🔒 You must join all required channels first.",
            reply_markup=join_keyboard(channels),
        )

    # Deep Link

    if context.args:

        code = context.args[0]

        return await handle_request_link(
            update,
            context,
            code,
        )

    settings = await settings_db.get()

    text = settings["start_text"]

    text = (
        text.replace(
            "{first_name}",
            user.first_name,
        )
        .replace(
            "{username}",
            user.username or "None",
        )
        .replace(
            "{id}",
            str(user.id),
        )
        .replace(
            "{bot_name}",
            context.bot.first_name,
        )
    )

    buttons = []

    for row in settings["start_buttons"]:

        btn_row = []

        for button in row:

            btn_row.append(
                InlineKeyboardButton(
                    button["text"],
                    url=button["url"],
                )
            )

        buttons.append(btn_row)

    markup = (
        InlineKeyboardMarkup(buttons)
        if buttons
        else None
    )

    if settings["start_photo"]:

        return await update.message.reply_photo(
            photo=settings["start_photo"],
            caption=text,
            reply_markup=markup,
        )

    await update.message.reply_text(
        text,
        reply_markup=markup,
    )


async def handle_request_link(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    code: str,
):

    # This will be implemented after links.py
    # and requests.py are completed.

    await update.message.reply_text(
        f"🔗 Request Code:\n\n<code>{code}</code>",
        parse_mode="HTML",
    )


start_handler = CommandHandler(
    "start",
    start,
    )
