"""Utility script to fetch all Fisherija locations and generate product URLs."""
import logging
from scraper import WoltScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Fetch all Fisherija locations and generate config."""
    print("\n" + "=" * 60)
    print("Fetching all Fisherija locations...")
    print("=" * 60 + "\n")

    with WoltScraper(headless=True) as scraper:
        # Get all locations from the brand page
        locations = scraper.get_all_fisherija_locations()

        if not locations:
            print("❌ No locations found. The page structure might have changed.")
            return

        print(f"✅ Found {len(locations)} locations:\n")

        # Product item ID from the example URL
        product_item_id = "divlji-crveni-losos-fileti-s-kozom-msc-150g-itemid-08c0c9d79b5528337e4ce2b1"

        print("Copy this configuration to your config.py file:\n")
        print("LOCATIONS = [")

        for i, location in enumerate(locations):
            # Extract venue slug from URL
            # Example: https://wolt.com/hr/hrv/zagreb/venue/fisherija-maksimir
            venue_slug = location['url'].split('/venue/')[-1].split('?')[0]

            # Construct product URL for this location
            product_url = f"https://wolt.com/hr/hrv/zagreb/venue/{venue_slug}/{product_item_id}"

            print(f"    {{")
            print(f"        'name': '{location['name']}',")
            print(f"        'url': '{product_url}'")
            print(f"    }},")

        print("]")

        print(f"\n{'=' * 60}")
        print("✅ Configuration generated successfully!")
        print("=" * 60)


if __name__ == '__main__':
    main()
