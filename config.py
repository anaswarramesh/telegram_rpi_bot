import os
from pathlib import Path

# Storage configuration
BASE_STORAGE_PATH = Path("/home/user/telegram_rpi")
PHOTO_STORAGE_PATH = BASE_STORAGE_PATH / "photos"
MESSAGE_STORAGE_PATH = BASE_STORAGE_PATH / "messages"
LOG_STORAGE_PATH = BASE_STORAGE_PATH / "logs"

# Create directories if they don't exist
for path in [PHOTO_STORAGE_PATH, MESSAGE_STORAGE_PATH, LOG_STORAGE_PATH]:
    path.mkdir(parents=True, exist_ok=True)

# Logging configuration
LOG_FILE = LOG_STORAGE_PATH / "telegram_bot.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Bot messages
WELCOME_MESSAGE = """👋 Welcome to Telegram RPi Bot!

I can help you save photos and messages to your Raspberry Pi.

📸 **Send a photo** - I'll save it with a timestamp
💬 **Send a message** - I'll save it to a text file

Use /help to see all available commands.
"""

HELP_MESSAGE = """📖 **Available Commands:**

/start - Show welcome message
/help - Show this help message

**How to use:**

📸 **Photos**: Just send a photo and I'll save it
💬 **Messages**: Send any text message and I'll save it to a .txt file

All files are saved with timestamps in:
- Photos: `/home/user/telegram_rpi/photos/`
- Messages: `/home/user/telegram_rpi/messages/`
"""

PHOTO_SAVED_MESSAGE = "✅ Photo saved successfully!\nFile: {filename}\nSize: {size} KB"
MESSAGE_SAVED_MESSAGE = "✅ Message saved successfully!\nFile: {filename}"
ERROR_MESSAGE = "❌ An error occurred: {error}"
