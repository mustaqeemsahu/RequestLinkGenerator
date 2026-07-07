from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
)

from database import channels_db

CHANNELS_PER_PAGE = 10


async def channels_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    page = int(query.data.split("_")[1])

    channels = await channels_db.get_channels_page(
        page,
        CHANNELS_PER_PAGE,
    )

    total = await channels_db.total_channels()

    pages = (total + CHANNELS_PER_PAGE - 1) // CHANNELS_PER_PAGE

    text = "<b>📺 Channels</b>\n\n"

    for i, ch in enumerate(
        channels,
        start=(page - 1) * CHANNELS_PER_PAGE + 1,
    ):

        text += (
            f"{i}. <b>{ch['title']}</b>\n"
            f"<code>{ch['channel_id']}</code>\n"
            f"🔗 {ch['short_code']}\n\n"
        )

    keyboard = []

    row = []

    if page > 1:

        row.append(
            InlineKeyboardButton(
                "⬅️ Previous",
                callback_data=f"channels_{page-1}",
            )
        )

    if page < pages:

        row.append(
            InlineKeyboardButton(
                "Next ➡️",
                callback_data=f"channels_{page+1}",
            )
        )

    if row:
        keyboard.append(row)

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


channels_callback_handler = CallbackQueryHandler(
    channels_callback,
    pattern=r"^channels_\d+$",
)
