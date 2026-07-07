from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def join_keyboard(channels):

    buttons = []

    for title, link in channels:

        buttons.append(
            [
                InlineKeyboardButton(
                    title,
                    url=link,
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "✅ Try Again",
                callback_data="checksub",
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)
