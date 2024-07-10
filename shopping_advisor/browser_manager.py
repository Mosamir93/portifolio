"""
This file contains the BrowserManager class for managing the Selenium Firefox browser instance.
"""
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

class BrowserManager:
    """
    A class to manage the Selenium Firefox
    browser instance with custom options.
    """
    def __init__(self):
        """
        Initialize the browser with custom options.
        """
        self.opts = Options()
        self.opts.add_argument("--headless")
        self.opts.add_argument('--no-sandbox')
        self.opts.add_argument('--disable-dev-shm-usage')
        self.opts.set_preference('permissions.default.stylesheet', 2)
        self.opts.set_preference("browser.cache.disk.enable", True)
        self.opts.set_preference("browser.cache.memory.enable", True)
        self.opts.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0")
        self.opts.set_preference("network.http.max-connections-per-server", 6)
        self.browser = Firefox(options=self.opts)

    def get_browser(self):
        """
        Get the initialized Firefox browser instance.
        """
        return self.browser
    
    def close_browser(self):
        """
        Close the Firefox browser instance.
        """
        self.browser.quit()
