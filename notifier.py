"""Telegram notification handler."""
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config import Config
import logging

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Handles sending notifications via Telegram."""

    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.chat_id = Config.TELEGRAM_CHAT_ID

    async def send_message(self, message):
        """Send a message to the configured chat."""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            logger.info(f"Notification sent: {message}")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    def send_message_sync(self, message):
        """Synchronous wrapper for sending messages."""
        try:
            asyncio.run(self.send_message(message))
        except Exception as e:
            logger.error(f"Error in send_message_sync: {e}")

    async def send_availability_alert(self, location_name, location_url, product_name, price=None):
        """Send a formatted availability alert."""
        price_text = f"\n💰 Price: {price}" if price else ""
        message = (
            f"🎉 <b>PRODUCT AVAILABLE!</b> 🎉\n\n"
            f"📦 {product_name}\n"
            f"📍 Location: {location_name}{price_text}\n\n"
            f"🔗 <a href='{location_url}'>Order Now!</a>"
        )
        await self.send_message(message)

    def send_availability_alert_sync(self, location_name, location_url, product_name, price=None):
        """Synchronous wrapper for sending availability alerts."""
        try:
            asyncio.run(self.send_availability_alert(location_name, location_url, product_name, price))
        except Exception as e:
            logger.error(f"Error sending availability alert: {e}")

    async def send_startup_message(self):
        """Send a message when the monitor starts."""
        message = (
            f"🚀 <b>Product Monitor Started</b>\n\n"
            f"Monitoring: {Config.PRODUCT_NAME}\n"
            f"Checking every {Config.CHECK_INTERVAL_MINUTES} minutes\n"
            f"Locations: {len(Config.LOCATIONS)}"
        )
        await self.send_message(message)

    def send_startup_message_sync(self):
        """Synchronous wrapper for sending startup message."""
        try:
            asyncio.run(self.send_startup_message())
        except Exception as e:
            logger.error(f"Error sending startup message: {e}")

    async def test_connection(self):
        """Test the Telegram bot connection."""
        try:
            me = await self.bot.get_me()
            logger.info(f"Telegram bot connected: @{me.username}")
            return True
        except TelegramError as e:
            logger.error(f"Failed to connect to Telegram: {e}")
            return False

    def test_connection_sync(self):
        """Synchronous wrapper for testing connection."""
        return asyncio.run(self.test_connection())
