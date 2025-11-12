"""Configuration management for the product tracker."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""

    # Telegram settings
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    # Monitoring settings
    CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', '5'))

    # Product settings
    PRODUCT_NAME = os.getenv('PRODUCT_NAME', 'Divlji crveni losos fileti s kožom MSC 150g')

    # Database
    DATABASE_PATH = 'product_tracker.db'

    # Wolt locations to monitor
    LOCATIONS = [
        {
            'name': 'Fisherija Maksimir',
            'url': 'https://wolt.com/hr/hrv/zagreb/venue/fisherija-maksimir/divlji-crveni-losos-fileti-s-kozom-msc-150g-itemid-08c0c9d79b5528337e4ce2b1'
        },
        # We'll add more locations after we can see them all
    ]

    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required. Please set it in .env file")
        if not cls.TELEGRAM_CHAT_ID:
            raise ValueError("TELEGRAM_CHAT_ID is required. Please set it in .env file")
        return True
