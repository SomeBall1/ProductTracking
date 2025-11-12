"""Telegram notification handler using simple requests."""
import requests
from config import Config
import logging

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handles sending notifications via Telegram using simple HTTP requests."""

    def __init__(self):
        self.token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, message, parse_mode='HTML'):
        """
        Send a message to the configured chat.

        Args:
            message: The message text to send
            parse_mode: 'HTML' or 'Markdown' or None

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message
            }
            if parse_mode:
                data['parse_mode'] = parse_mode

            response = requests.post(url, data=data, timeout=10)

            if response.status_code == 200:
                logger.info(f"Notification sent successfully")
                return True
            else:
                logger.error(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")
                return False

        except requests.RequestException as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

    def send_availability_alert(self, location_name, location_url, product_name, price=None):
        """Send a formatted availability alert."""
        price_text = f"\n💰 Price: {price}" if price else ""
        message = (
            f"🎉 <b>PRODUCT AVAILABLE!</b> 🎉\n\n"
            f"📦 {product_name}\n"
            f"📍 Location: {location_name}{price_text}\n\n"
            f"🔗 <a href='{location_url}'>Order Now!</a>"
        )
        return self.send_message(message)

    def send_startup_message(self):
        """Send a message when the monitor starts."""
        message = (
            f"🚀 <b>Product Monitor Started</b>\n\n"
            f"Monitoring: {Config.PRODUCT_NAME}\n"
            f"Checking every {Config.CHECK_INTERVAL_MINUTES} minutes\n"
            f"Locations: {len(Config.LOCATIONS)}"
        )
        return self.send_message(message)

    def test_connection(self):
        """Test the Telegram bot connection."""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data.get('result', {})
                    username = bot_info.get('username', 'Unknown')
                    logger.info(f"Telegram bot connected: @{username}")
                    return True

            logger.error(f"Failed to connect to Telegram. Status: {response.status_code}")
            return False

        except requests.RequestException as e:
            logger.error(f"Failed to connect to Telegram: {e}")
            return False

    # For compatibility with old code, keep the _sync methods but they're not needed anymore
    def send_message_sync(self, message):
        """Send a message (compatibility method)."""
        return self.send_message(message)

    def send_availability_alert_sync(self, location_name, location_url, product_name, price=None):
        """Send availability alert (compatibility method)."""
        return self.send_availability_alert(location_name, location_url, product_name, price)

    def send_startup_message_sync(self):
        """Send startup message (compatibility method)."""
        return self.send_startup_message()

    def test_connection_sync(self):
        """Test connection (compatibility method)."""
        return self.test_connection()
