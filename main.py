import os
import requests
import undetected_chromedriver as uc
from scrapper_boilerplate import explicit_wait
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from time import sleep
from user_secrets import bearer_token, akamai_telemetry


DEBUG = True


def login(driver):
    driver.get('https://www.maersk.com/instantPrice/')
        # driver.implicitly_wait(220)
    explicit_wait(driver, By.TAG_NAME, 'body')

    if driver.current_url != "https://www.maersk.com/portaluser/login":
        return

    # if driver.find_element(By.TAG_NAME, 'title').text == 'Sign In':
    username_field = driver.find_element(By.CSS_SELECTOR, 'input[name="usernameInput"]')
    username_field.clear()
    username_field.send_keys(os.getenv('MAESK_LOGIN'))
    
    password_field = driver.find_element(By.CSS_SELECTOR, 'input[name="passwordInput"]')
    password_field.clear()
    password_field.send_keys(os.getenv('MAESK_PASSWORD'))

    # driver.find_element(By.ID, 'rm').click()
    driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/div/label').click()
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    sleep(10)


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
    send_button = driver.find_element(By.CSS_SELECTOR, 'button.button--primary').click()


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


def get_ship_price(bearer_token="", akamai_telemetry=""):

    url = "https://api.maersk.com/productoffer/v2/productoffers"

    payload = {
        "from": {
            "name": "Santos (Sao Paulo), Brazil",
            "maerskGeoId": "1BX66GARX9UAH",
            "countryCode": "BR",
            "maerskServiceMode": "CY",
            "maerskRkstCode": "BRSSZ"
        },
        "to": {
            "name": "Singapore, Singapore",
            "maerskGeoId": "0XOP5ISJZK0HR",
            "countryCode": "SG",
            "maerskServiceMode": "CY",
            "maerskRkstCode": "SGSIN"
        },
        "commodity": {
            "id": "001413",
            "name": "(With Lithium Batteries) Electronics, electronic appliances, audio, video equipment, telecommunication equipment",
            "isDangerous": False,
            "dangerousDetails": []
        },
        "containers": [
            {
                "isoCode": "22G1",
                "name": "20 Dry Standard",
                "size": "20",
                "type": "DRY",
                "weight": 18000,
                "quantity": 1,
                "isReefer": False,
                "isNonOperatingReefer": False,
                "isShipperOwnedContainer": False
            }
        ],
        "unit": "KG",
        "shipmentPriceCalculationDate": "2022-10-26",
        "brandCode": "MAEU",
        "customerCode": "30501103219",
        "isSameRequest": False,
        "loadAFLS": False,
        "weekOffset": 0
    }
    
    headers = {
        "authority": "api.maersk.com",
        "accept": "application/json, text/plain, */*",
        "akamai-bm-telemetry": akamai_telemetry,
        "authorization": bearer_token,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f'Erro: {response.status_code}!\n verifique as suas credenciais...')

    return response.json()


def main():
    
    driver = uc.Chrome(version_main=105)
    driver.set_window_size(1400, 1000)
    try:
        login(driver)
    
    except ElementClickInterceptedException:
        explicit_wait(driver, By.CSS_SELECTOR, 'button[aria-label="Allow all"]').click()
        login(driver)

    pick_cargo(driver)
    display_info(driver)
    data = get_ship_price(bearer_token=bearer_token, akamai_telemetry=akamai_telemetry)
    print(data)


if __name__ == "__main__":
    main()