import unittest
from src.webdriver import get_proxy
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from scrapper_boilerplate.setup import init_log
from webdriver_manager.chrome import ChromeDriverManager
import logging
from time import sleep


class TestProxy(unittest.TestCase):
    def setUp(self) -> None:
        init_log()
        self.proxy = get_proxy()

    def test_proxies(self):
        logging.info('Getting token')
        options = Options()
        logging.info('Setting...')

        # options.headless = True
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--proxy-server={}'.format(self.proxy))  
        driver = Chrome(ChromeDriverManager().install(), options=options)
    
        driver.set_window_size(1200, 900)
        logging.info('Viewing ip address...')
        driver.get('https://whatismyipaddress.com/')
        sleep(30)


if __name__ == "__main__":
    unittest.main()
