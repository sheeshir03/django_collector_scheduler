# scraper_scripts/dummy_scraper.py

import json
import sys
from datetime import datetime
import time

def scrape():

    time.sleep(30)
    """
    Simulates a scraping process by generating mock data.
    """
    try:
        # Simulate scraping delay
        time.sleep(2)  # Sleep for 2 seconds to mimic processing time

        # Generate mock data
        data = {
            "links": [
                "https://example.com",
            ],
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }

        # Output JSON data
        print(json.dumps(data))
    except Exception as e:
        # Output error information in JSON format
        error_data = {
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
        print(json.dumps(error_data))
        sys.exit(1)  # Exit with a non-zero status to indicate failure

if __name__ == "__main__":
    scrape()
