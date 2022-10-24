import os
import logging

from scrapper_boilerplate import explicit_wait, setSelenium
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from time import sleep
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from src.utils import get_free_proxies

DEBUG = True

def get_proxy():
    """
    get a new proxy

    return: str: proxy url
    """
    logging.info('getting new proxy')
    with setSelenium(headless=True, remote_webdriver=True) as driver:
        proxies = get_free_proxies(driver)
        target_proxy = None
        for proxy in proxies:
            target_proxy = proxy['IP Address']
            break

    logging.info(f'proxy {target_proxy} found!')


def get_token(new_bearer=False):
    if os.path.exists('bearer.txt') and not new_bearer:
        with open('bearer.txt') as bearer_file:
            data = bearer_file.read()

        return data

    logging.info('Getting token')
    options = Options()
    logging.info('Setting...')

    options.headless = True
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    # proxy = get_proxy()
    # options.add_argument('--proxy-server={}'.format(proxy))
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    driver.set_window_size(1200, 900)
    logging.info('Navigating to login...')
    driver.get('https://www.maersk.com/portaluser/login')
    login(driver)

    for request in driver.requests:
        if request.headers['Authorization'] and request.headers['Authorization'].startswith('Bearer'):
            print(request.headers['Authorization'])
            bearer = request.headers['Authorization']
            driver.quit()

            if bearer or not bearer.endswith('null'):
                with open('bearer.txt', 'w') as bearer_file:
                    bearer_file.write(bearer)

            return bearer

    return


def login(driver):
        
    try:
        explicit_wait(driver, By.TAG_NAME, 'body')

        if driver.current_url != "https://www.maersk.com/portaluser/login":
            return

        # if driver.find_element(By.TAG_NAME, 'title').text == 'Sign In':
        logging.info('Inserting username...')
        username_field = driver.find_element(By.CSS_SELECTOR, 'input[name="usernameInput"]')
        username_field.clear()
        username_field.send_keys(os.getenv('MAESK_LOGIN'))
        logging.info('Done!')

        logging.info('Inserting password...')
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[name="passwordInput"]')
        password_field.clear()
        password_field.send_keys(os.getenv('MAESK_PASSWORD'))
        logging.info('Done!')

        # driver.find_element(By.ID, 'rm').click()
        logging.info('Cheching ID...')
        driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/div/label').click()
        logging.info('Done!')

        logging.info('click Logging...')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        # driver.save_screenshot('logging.png')
        logging.info('Waiting')
        explicit_wait(driver, By.CSS_SELECTOR, 'h1.hub__header__title', timeout=220)
        # sleep(30)
        # driver.save_screenshot('logging-2.png')
        # sleep(90)
        logging.info('Done!')

    except ElementClickInterceptedException:
        logging.info('Retryng...')
        driver.find_element(By.XPATH, '//button[text()="Allow all"]').click()
        login(driver)

    except Exception:
        driver.save_screenshot('error.png')
        raise


def pick_cargo(driver):

    if DEBUG:
        input('Preencha os campos e aperte ENTER para continuar...')
        return

    from_field = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="Enter city name"]')[0]
    from_field.send_keys('Santos (Sao Paulo), Brazil')

    to_field = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="Enter city name"]')[1]
    to_field.send_keys('Singapore, Singapore')

    # commodity name
    commodity_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter Commodity"]')
    commodity_field.send_keys('(With Lithium Batteries) Electronics, electronic appliances, audio, video equipment, telecommunication equipment')
    
    # commodity type
    commodity_type_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Select container type"]')
    commodity_type_field.send_keys('20 Dry Standard')

    # placeholder="Select Date"
    # date
    commodity_type_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Select Date"]')
    commodity_type_field.send_keys('05/10/2022')

    # send
    driver.find_element(By.CSS_SELECTOR, 'button.button--primary').click()


def display_info(driver):
    info_container = explicit_wait(driver, By.CSS_SELECTOR, '.basic-card.base-card2')

    price = driver.find_element(By.CSS_SELECTOR, '.total-price--amount.scol-4')
    print(price.text)

    departure = info_container.find_element(By.XPATH,'//*[@id="webapp"]/div/article/section/div[1]/section/div[5]/div[3]/section[1]/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div')
    print(departure.text)

    transit_info = info_container.find_element(By.XPATH, '//*[@id="webapp"]/div/article/section/div[1]/section/div[5]/div[3]/section[1]/div[3]/div/div[1]/div/div[2]/div/div[2]')
    print(transit_info.text)
    arrival = info_container.find_element(By.XPATH, '//*[@id="webapp"]/div/article/section/div[1]/section/div[5]/div[3]/section[1]/div[3]/div/div[1]/div/div[2]/div/div[2]')
    print(arrival.text)
