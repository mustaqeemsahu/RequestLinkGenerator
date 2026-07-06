import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")

OWNER_ID = int(os.getenv("OWNER_ID"))

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

PORT = int(os.getenv("PORT", 10000))


BOT_NAME = "Request Manager"

VERSION = "1.0"


LINK_EXPIRE = 60


LOG_LEVEL = "INFO"


DATABASE_NAME = "RequestBot"


MAX_CHANNELS = 1000


BROADCAST_SLEEP = 0.05


AUTO_DELETE_EXPIRED = True
