from ..browser_manager import BrowserManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import urllib.parse

def scrape_hyperone(search_term):
    browser_manager = BrowserManager()
    browser = browser_manager.get_browser()
    try:
        encoded_search_term = urllib.parse.quote(search_term)
        search_url = f"https://www.hyperone.com.eg/search?q={encoded_search_term}&sortBy=relevance&sortOrder=DESC"
        browser.get(search_url)
        browser.find_elements(By.CLASS_NAME, "ProductTitle")

        try:
            no_results_element = browser.find_elements(By.XPATH, "//svg[@data-v-66b7c9b4 and @data-v-42178517]")
            if no_results_element:
                return []
        except NoSuchElementException:
            pass

        html_content = browser.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        product_cards = soup.find_all('div', class_='flex items-baseline text-primary-700 font-bold mt-auto text-lg')
        products = []

        for card in product_cards:
            name_tag = card.find_previous('p', {'class': 'ProductTitle text-sm mt-2 text-system-gray w-full'})
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'
            price_whole_tag = card.find('span', {'data-v-6750406f': ''})
            price_currency_tag = card.find('span', {'class': 'Currency ml-1'})
            price = f"{price_whole_tag.get_text(strip=True)} {price_currency_tag.get_text(strip=True)}"
            img_tag = card.find_previous('picture').find('img')
            img_url = img_tag['src'] if img_tag else 'N/A'

            products.append({
                'name': name,
                'price': price,
                'img_url': img_url,
                'vendor': 'Hyperone'
            })


    except TimeoutException:
        return []
    finally:
        browser_manager.close_browser()
    return products
