import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.scraper import scrape_ajio, scrape_snitch

if __name__ == '__main__':
    print("--- Testing Ajio Scraper for 'red t-shirt' ---")
    ajio_results = scrape_ajio("red t-shirt")
    if ajio_results:
        print(f"Ajio scraper returned {len(ajio_results)} results.")
        for product in ajio_results:
            print(product)
    else:
        print("Ajio scraper returned no results.")

    print("\n" + "="*30 + "\n")

    print("--- Testing Snitch Scraper for 'black shirt' ---")
    snitch_results = scrape_snitch("black shirt")
    if snitch_results:
        print(f"Snitch scraper returned {len(snitch_results)} results.")
        for product in snitch_results:
            print(product)
    else:
        print("Snitch scraper returned no results.")

    print("\nScraper tests finished.")
