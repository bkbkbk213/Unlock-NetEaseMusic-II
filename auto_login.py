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
    browser.add_cookie({"name": "MUSIC_U", "value": "009CA6605FC2F3E0562A67224BDAFA839E6269C3B9DBC187C553A0BC21D90AB19AD250390EA7B8CD1FCAA183E5AFBEB6C9F734B816978701212B3FA614BC88AA19D8CE6CDAACF4A10B95CECAE626243BBD1E924757C637243C3F57B4A4FBFC609A1D0E523B2F98AF41CEEE708C78AB2FB46F4EB254ED1FBC8D074B04ED6F66824B39A9F5E80A4BC788AC09C635974FDEDF3A83F1F97BA4A3969C7BAE5005753C5593C6CBE20A441EC0D9FD8D5CDB251E50E46485C107F753BDEF5A5EF953C9E98493FB0766FA51BCE387952FB3D6AE048F21D0A8F246E4C856103B4B1371547064041E6E69633FAFD0B47E5A2A43087FA41F4D2C175993461141985D40DFA47FF0E4E6C813F74E4686A97625DEC8C9E8E1368AF761DF5A62BA8B87B66B950C6A0300EE1838B7644CAF0280D9C5F4156F137BDE394EADAD6A4B1474298F5411B95702C079ED2B203681055E9E609A873286AB4E779E562AEB3AAEAEC178776F2543"
Privacy and security panel
Test how a website behaves with limited third-party cookies and find relevant issues in the new 'Privacy' section of the evolved 'Privacy and security' panel.

Calibrated CPU throttling presets
Based on your users' experience, automatically calibrate and use more accurate CPU throttling presets for low- and mid-tier mobile devices.

First- and third-party highlighting in Performance
Reduce the noise of third-party data and hover over entries in a new table in Summary to distinguish between first- and third-party data in performance traces."})
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
