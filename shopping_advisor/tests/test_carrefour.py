import unittest
from shopping_advisor.scrapers.carrefour_scraper import scrape_carrefour

class TestCarrefourScraper(unittest.TestCase):
    def test_scrape_carrefour(self):
        results = scrape_carrefour('bread')
        self.assertGreater(len(results), 0, "No results found for 'bread'")
        print(results)

if __name__ == '__main__':
    unittest.main()
