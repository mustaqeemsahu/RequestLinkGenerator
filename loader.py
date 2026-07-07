import logging

from telegram.ext import Application

from config import BOT_TOKEN
from database import db

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("RequestBot")


application = (
    Application.builder()
    .token(BOT_TOKEN)
    .build()
)


async def startup(app: Application):
    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    logger.info("Starting Request Manager Bot...")

    try:
        await db.ping()
        logger.info("✅ MongoDB Connected")
    except Exception as e:
        logger.error(f"MongoDB Error: {e}")
        raise

    await db.create_indexes()

    logger.info("✅ Database Indexes Loaded")
    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


async def shutdown(app: Application):
    logger.info("Stopping Bot...")

    db.client.close()

    logger.info("MongoDB Connection Closed")


application.post_init = startup
application.post_shutdown = shutdown
