"""Main product availability monitor."""
import logging
import time
import schedule
from datetime import datetime
from database import Database
from scraper import WoltScraper
from notifier import TelegramNotifier
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('product_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProductMonitor:
    """Main product monitoring class."""

    def __init__(self):
        self.db = Database()
        self.notifier = TelegramNotifier()
        self.scraper = None

    def check_all_locations(self):
        """Check product availability at all configured locations."""
        logger.info(f"Starting check cycle at {datetime.now()}")

        # Initialize scraper for this check cycle
        with WoltScraper(headless=True) as scraper:
            for location in Config.LOCATIONS:
                try:
                    self._check_location(location, scraper)
                    time.sleep(2)  # Be nice to the server
                except Exception as e:
                    logger.error(f"Error checking location {location['name']}: {e}")

        logger.info("Check cycle completed")

    def _check_location(self, location, scraper):
        """Check a single location for product availability."""
        location_name = location['name']
        location_url = location['url']

        logger.info(f"Checking {location_name}...")

        # Get the last check for this location
        last_check = self.db.get_last_check(location_name)

        # Check current availability
        result = scraper.check_product_availability(location_url)

        if result['error']:
            logger.error(f"Error checking {location_name}: {result['error']}")
            return

        # Save to database
        self.db.add_check(
            location_name=location_name,
            location_url=location_url,
            product_name=Config.PRODUCT_NAME,
            is_available=result['available'],
            price=result['price']
        )

        # Check if we should send a notification
        # Send notification if:
        # 1. Product is now available AND
        # 2. (First check OR was not available before)
        should_notify = (
            result['available'] and
            (last_check is None or not last_check.is_available)
        )

        if should_notify:
            logger.info(f"🎉 Product became available at {location_name}!")
            self.notifier.send_availability_alert_sync(
                location_name=location_name,
                location_url=location_url,
                product_name=Config.PRODUCT_NAME,
                price=result['price']
            )
        else:
            status = "available" if result['available'] else "not available"
            logger.info(f"{location_name}: {status}")

    def run(self):
        """Run the monitoring loop."""
        logger.info("=" * 60)
        logger.info("Product Monitor Starting")
        logger.info("=" * 60)

        # Validate configuration
        try:
            Config.validate()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            return

        # Test Telegram connection
        if not self.notifier.test_connection_sync():
            logger.error("Failed to connect to Telegram. Please check your bot token and chat ID.")
            return

        # Send startup notification
        self.notifier.send_startup_message_sync()

        logger.info(f"Monitoring {len(Config.LOCATIONS)} location(s)")
        logger.info(f"Check interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
        logger.info(f"Product: {Config.PRODUCT_NAME}")

        # Do an initial check immediately
        try:
            self.check_all_locations()
        except Exception as e:
            logger.error(f"Error in initial check: {e}")

        # Schedule periodic checks
        schedule.every(Config.CHECK_INTERVAL_MINUTES).minutes.do(self.check_all_locations)

        logger.info("Entering monitoring loop... (Press Ctrl+C to stop)")

        # Run the scheduler
        try:
            while True:
                schedule.run_pending()
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up...")
        self.db.close()


def main():
    """Main entry point."""
    monitor = ProductMonitor()
    monitor.run()


if __name__ == '__main__':
    main()
