from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def scrape_oscar(search_term):
    opts = Options()
    opts.add_argument("--headless")
    browser = Firefox(options=opts)

    try:
        browser.get("https://www.oscarstores.com/products_search")

        # Wait for search box to be present and then find it by ID
        search_box = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.ID, "search_input"))
        )

        search_box.send_keys(search_term)
        search_box.submit()

        try:
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "card"))
            )
        except TimeoutException:
            print(f"No results found for '{search_term}' on Oscar")
            return []       

        # Get the updated page source after search
        html_content = browser.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all product cards
        product_cards = soup.find_all('div', class_='card position-relative p-2 rounded-2 border-0 mx-1 w-100 h-100')

        products = []

        for card in product_cards:
            name_tag = card.find('h5', class_='my-2 one-lines ellipse text-left f_oswald c_black f-16 text-capitalize f-w_bold')
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'

            price_tag = card.find('span', class_='c_red f-15')
            price = price_tag.get_text(strip=True) if price_tag else 'N/A'

            price = ' '.join(price.split())

            img_tag = card.find('img')
            img_url = img_tag['src'] if img_tag else 'N/A'

            products.append({
                'name': name,
                'price': price,
                'img_url': img_url,
                'vendor': 'Oscar'
            })



    finally:
        browser.close()
        browser.quit()
    return products
