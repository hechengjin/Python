from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from config import *

def byChrome():
    try:
        browser = webdriver.Chrome()
        browser.get('https://www.baidu.com')
        input = browser.find_element_by_id('kw')
        input.send_keys('Python')
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID,'content_left')))
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)
    finally:
        browser.close()
def byPhantomJS():
    try:
        browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        browser.set_window_size(1400, 900)
        browser.get('https://www.baidu.com')
        input = browser.find_element_by_id('kw')
        input.send_keys('Python')
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)
    finally:
        browser.close()

def main():
    byPhantomJS()
    #byChrome()

if __name__ == '__main__':
    main()