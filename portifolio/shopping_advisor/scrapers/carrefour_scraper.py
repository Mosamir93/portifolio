from ..browser_manager import BrowserManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import urllib.parse

def scrape_carrefour(search_term):
    browser_manager = BrowserManager()
    browser = browser_manager.get_browser()
    try:
        encoded_search_term = urllib.parse.quote(search_term)
        search_url = f"https://www.carrefouregypt.com/mafegy/en/v4/search?keyword={encoded_search_term}"
        browser.get(search_url)
        browser.find_element(By.CLASS_NAME, "css-yqd9tx")

        try:
            no_result_text = browser.find_element(By.CSS_SELECTOR, '[data-testid="no-result-text"]')
            if no_result_text:
                return []
        except NoSuchElementException:
            pass

        html_content = browser.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        product_cards = soup.find_all('div', class_='css-yqd9tx')
        products = []

        for card in product_cards:
            name_tag = card.find('a', {'data-testid': 'product_name'})
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'
            price_whole_tag = card.find('div', class_='css-14zpref')
            price_fraction_tag = card.find('div', class_='css-1pjcwg4')
            price_currency_tag = card.find('span', class_='css-1edki26')
            price = f"{price_whole_tag.get_text(strip=True)}{price_fraction_tag.get_text(strip=True)} {price_currency_tag.get_text(strip=True)}"
            img_tag = card.find('img', {'data-testid': 'product_image_main'})
            img_url = img_tag['src'] if img_tag else 'N/A'

            products.append({
                'name': name,
                'price': price,
                'img_url': img_url,
                'vendor': 'Carrefour'
            })

    except TimeoutException:
        return []
    finally:
        browser_manager.close_browser()
    return products
