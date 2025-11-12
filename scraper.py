"""Web scraper for Wolt product availability."""
import logging
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class WoltScraper:
    """Scrapes Wolt website for product availability."""

    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def start(self):
        """Initialize the browser."""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.context = self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            logger.info("Browser initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    def close(self):
        """Close the browser."""
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")

    def check_product_availability(self, url, timeout=30000):
        """
        Check if a product is available at a given Wolt URL.

        Args:
            url: The Wolt product URL
            timeout: Page load timeout in milliseconds

        Returns:
            dict: {
                'available': bool,
                'price': str or None,
                'error': str or None
            }
        """
        if not self.context:
            self.start()

        page = None
        try:
            page = self.context.new_page()
            logger.info(f"Navigating to: {url}")

            # Navigate to the page
            page.goto(url, wait_until='networkidle', timeout=timeout)

            # Wait a bit for dynamic content to load
            time.sleep(2)

            # Get the page content
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')

            # Check for "out of stock" indicators
            # Wolt typically shows "Sold out" or similar text
            page_text = soup.get_text().lower()

            # Common indicators that product is NOT available
            out_of_stock_indicators = [
                'sold out',
                'rasprodano',
                'nije dostupno',
                'out of stock',
                'not available'
            ]

            is_out_of_stock = any(indicator in page_text for indicator in out_of_stock_indicators)

            # Try to find price (if available, product is likely in stock)
            price = None
            # Look for price patterns (e.g., "€12.99" or "12,99 €")
            price_elements = soup.find_all(text=lambda text: text and '€' in text)
            if price_elements:
                for elem in price_elements:
                    if any(char.isdigit() for char in elem):
                        price = elem.strip()
                        break

            # Determine availability
            # If we found a price and no out-of-stock indicators, it's likely available
            available = price is not None and not is_out_of_stock

            logger.info(f"Check result - Available: {available}, Price: {price}, Out of stock indicator: {is_out_of_stock}")

            return {
                'available': available,
                'price': price,
                'error': None
            }

        except PlaywrightTimeout:
            logger.error(f"Timeout loading page: {url}")
            return {
                'available': False,
                'price': None,
                'error': 'Timeout loading page'
            }
        except Exception as e:
            logger.error(f"Error checking product availability: {e}")
            return {
                'available': False,
                'price': None,
                'error': str(e)
            }
        finally:
            if page:
                page.close()

    def get_all_fisherija_locations(self, brand_url="https://wolt.com/hr/hrv/zagreb/brand/fisherija"):
        """
        Scrape all Fisherija locations from the brand page.

        Returns:
            list: List of dicts with location info
        """
        if not self.context:
            self.start()

        page = None
        try:
            page = self.context.new_page()
            logger.info(f"Fetching locations from: {brand_url}")

            page.goto(brand_url, wait_until='networkidle', timeout=30000)
            time.sleep(3)  # Wait for dynamic content

            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')

            locations = []

            # Find location links - these are typically in <a> tags with venue links
            venue_links = soup.find_all('a', href=lambda href: href and '/venue/' in href)

            for link in venue_links:
                href = link.get('href')
                # Make absolute URL if needed
                if href.startswith('/'):
                    href = f"https://wolt.com{href}"

                # Extract location name from the link text or nearby elements
                name = link.get_text(strip=True)

                if href and name and href not in [loc['url'] for loc in locations]:
                    locations.append({
                        'name': name,
                        'url': href
                    })

            logger.info(f"Found {len(locations)} locations")
            return locations

        except Exception as e:
            logger.error(f"Error fetching locations: {e}")
            return []
        finally:
            if page:
                page.close()
