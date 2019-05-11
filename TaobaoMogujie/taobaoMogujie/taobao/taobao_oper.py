from selenium import webdriver
from selenium.common import exceptions
import time
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *

#实例化一个Chrome浏览器的配置选项
#chrome_option = webdriver.ChromeOptions()
#chrome_option.add_argument('--proxy-server=127.0.0.1:1080')
browser = webdriver.Chrome()
#browser = webdriver.Chrome(executable_path=r"D:\ProgramFiles\Anaconda3\Scripts\chromedriver.exe",options=chrome_option)
browser.maximize_window()
wait = WebDriverWait(browser, 10)


def login():
    # 1.登陆
    try:
        browser.get(URL_LOGIN)
    except exceptions.TimeoutException:  # 当页面加载时间超过设定时间，JS来停止加载
        browser.execute_script('window.stop()')

    count = 0
    while count < 5:  # 重试5次
        count += 1
        if login_one() is True:
            break
    if count == 5:
        return False

def login_one():
    try:
        # 1.点击密码登录，切换到密码登录模式 默认是二维码登录
        username_login_btn = browser.find_element_by_xpath("//a[@class='forget-pwd J_Quick2Static']")
        if username_login_btn.is_displayed() is True:
            username_login_btn.click()
    except exceptions.ElementNotInteractableException:
        pass
    # 2.获取账户、密码输入框
    username_input = browser.find_element_by_id("TPL_username_1")
    password_input = browser.find_element_by_id("TPL_password_1")
    # 3.为账户、密码赋值
    username_input.clear()
    username_input.send_keys(USER_NAME)
    password_input.send_keys(USER_PASSWORD)

    # 4.滑块判断
    login_slide()

    # 5.获取登陆按钮，并点击登录
    submit_btn = browser.find_element_by_id("J_SubmitStatic")
    submit_btn.click()
    # 6.根据提示判断是否登录成功
    try:
        message = browser.find_element_by_id("J_Message").find_element_by_class_name("error")
        if message.text == u"为了你的账户安全，请拖动滑块完成验证":
            browser.execute_script(
                "document.getElementById('J_Message').children[1].innerText='查货机器人：请滑动滑块，协助完成验证！';")
            return False
    except exceptions.NoSuchElementException:
        pass

    # 7.有时检测当前环境是否异常，此时休眠一段时间让它检测
    while True:
        try:
            browser.find_element_by_id("J_SiteNav")
            break
        except exceptions.NoSuchElementException:
            time.sleep(1)

    return True

def login_slide():
    # 取得滑块所在div，判断是否display 一般首次登陆不需要滑块验证
    slide_div = browser.find_element_by_id("nocaptcha")
    if slide_div.is_displayed() is True:
        browser.execute_script(
            "document.getElementById('J_Message').children[1].innerText='查货机器人：请滑动滑块，协助完成验证！';")
        while True:
            try:
                text = browser.find_element_by_id("nc_1__scale_text").text
                if text == '验证通过':
                    break
                time.sleep(0.5)
            except exceptions.NoSuchElementException:  # 此时处于刷新按钮状态
                pass

def main():
    login()

if __name__ == '__main__':
    main()