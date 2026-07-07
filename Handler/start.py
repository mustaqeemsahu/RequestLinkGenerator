from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome to Request Manager Bot!\n\n"
        "Bot is running successfully."
    )


start_handler = CommandHandler(
    "start",
    start,
)
