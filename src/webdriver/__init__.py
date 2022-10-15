import os
import requests
import undetected_chromedriver as uc
from scrapper_boilerplate import explicit_wait
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from time import sleep

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
