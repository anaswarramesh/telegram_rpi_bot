#!/usr/bin/env python3
"""
Telegram Bot for Raspberry Pi
Saves photos and messages to local storage
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=config.LOG_FORMAT,
    datefmt=config.LOG_DATE_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class TelegramRpiBot:
    """Telegram bot for Raspberry Pi file storage"""

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN not found in environment variables. "
                "Please set it in .env file"
            )
        logger.info("Bot initialized successfully")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send welcome message on /start command"""
        logger.info(f"User {update.effective_user.id} started the bot")
        await update.message.reply_text(config.WELCOME_MESSAGE)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send help message on /help command"""
        logger.info(f"User {update.effective_user.id} requested help")
        await update.message.reply_text(config.HELP_MESSAGE)

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming photos"""
        try:
            user_id = update.effective_user.id
            photo = update.message.photo[-1]  # Get highest resolution photo

            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
            filename = f"photo_{timestamp}.jpg"
            filepath = config.PHOTO_STORAGE_PATH / filename

            # Download and save photo
            file = await context.bot.get_file(photo.file_id)
            await file.download_to_drive(filepath)

            # Get file size
            file_size = filepath.stat().st_size / 1024  # Convert to KB

            logger.info(
                f"User {user_id} saved photo: {filename} ({file_size:.2f} KB)"
            )

            # Send confirmation
            confirmation = config.PHOTO_SAVED_MESSAGE.format(
                filename=filename, size=f"{file_size:.2f}"
            )
            await update.message.reply_text(confirmation)

        except Exception as e:
            logger.error(f"Error handling photo: {str(e)}")
            await update.message.reply_text(
                config.ERROR_MESSAGE.format(error=str(e))
            )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming text messages"""
        try:
            user_id = update.effective_user.id
            message_text = update.message.text

            # Create filename with date
            date = datetime.now().strftime("%Y-%m-%d")
            filename = f"{date}.txt"
            filepath = config.MESSAGE_STORAGE_PATH / filename

            # Create timestamp for the message
            time_str = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{time_str}] {message_text}\n"

            # Append message to file
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(formatted_message)

            logger.info(
                f"User {user_id} saved message to {filename}: {message_text[:50]}..."
            )

            # Send confirmation
            confirmation = config.MESSAGE_SAVED_MESSAGE.format(filename=filename)
            await update.message.reply_text(confirmation)

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await update.message.reply_text(
                config.ERROR_MESSAGE.format(error=str(e))
            )

    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")

        # Create application
        application = Application.builder().token(self.token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(
            MessageHandler(filters.PHOTO, self.handle_photo)
        )
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        # Start polling
        logger.info("Bot is running and listening for messages...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        bot = TelegramRpiBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise
