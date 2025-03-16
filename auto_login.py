# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00E0B30260C8C5BD2F4696B410D8F9CBB5E14CD2B169DA5FAEAAE18DA77DD2E7C2A6DAF040708432326A36D9D0FBDEE53450EC1F37C84BFD6D75FA9FF5B62A09FEB9F02F0C6051296E01EFA8FF79DDC1598C3DFD0B51BBD4A83C20FC8C0C9F96353A86A16C26363CD22E6F9DA851F29192BB424D14459B889EB05A46A6723447624D666B8EE5DD5440922261707F5F5F972AC09EB93A4588A131B2B067D983E252DCF60679F184A609C5843AB959B4331A7B8E0CEC2B5812CB726D5C97E1A9204E92806E38C37F0ACC980F85E6290544EC10F87F901D5FAA5A9DAE04512F77F77EADBEA77CBE8BEB85C3FB200BFE676C740CE01CCC142355EDF589F6B59F7749A85F720F373D16C8A176E332D284831A3211376FFEE1574151319805E8EB795A7F7F35E73050A82511C605AE57EF289273B357A360E3B4C0C6E55AC037C05A85A32E0D45AFB730DF52B0DA18E45EC7595EDAD26842811470085B4B5AD116220D6B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
