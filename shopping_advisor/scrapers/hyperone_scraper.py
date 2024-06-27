from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import urllib.parse

def scrape_hyperone(search_term):
    opts = Options()
    opts.add_argument("--headless")

    # Initialize the browser
    browser = Firefox(options=opts)

    try:
        encoded_search_term = urllib.parse.quote(search_term)

        # Construct the search URL
        search_url = f"https://www.hyperone.com.eg/search?q={encoded_search_term}&sortBy=relevance&sortOrder=DESC"
        
        # Open the search URL
        browser.get(search_url)
        print(f"Page loaded successfully with search term '{search_term}'")

        try:
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ProductTitle"))
            )
            print("Search results loaded")
        except TimeoutException:
            print(f"No results found for '{search_term}' on Hyperone")
            return []

        try:
            no_result_svg = browser.find_element(By.CSS_SELECTOR, 'svg.icon.sprite-icons')
            if no_result_svg:
                print(f"No results found for '{search_term}' on Hyperone")
                return []
        except NoSuchElementException:
            pass       

        # Get the updated page source after search
        html_content = browser.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all product cards
        product_cards = soup.find_all('div', class_='flex items-baseline text-primary-700 font-bold mt-auto text-lg')

        # List to hold product information
        products = []

        for card in product_cards:
            # Extract the product name
            name_tag = card.find_previous('p', {'class': 'ProductTitle text-sm mt-2 text-system-gray w-full'})
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'

            # Extract the product price
            price_whole_tag = card.find('span', {'data-v-6750406f': ''})
            price_currency_tag = card.find('span', {'class': 'Currency ml-1'})

            price_whole = price_whole_tag.get_text(strip=True) if price_whole_tag else 'N/A'
            price_currency = price_currency_tag.get_text(strip=True) if price_currency_tag else 'N/A'
            
            price = f"{price_whole} {price_currency}"

            # Extract the product image URL
            img_tag = card.find_previous('picture').find('img')
            img_url = img_tag['src'] if img_tag else 'N/A'

            products.append({
                'name': name,
                'price': price,
                'img_url': img_url,
                'vendor': 'Hyperone'
            })


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the browser closes properly
        browser.close()
        browser.quit()
        print("Browser closed")
    return products
