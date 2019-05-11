#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import random
import time
from pyppeteer import launch
from retrying import retry
from config import *

import xlrd
import xlwt

file = 'orders.xls'
row_list = []
res_list = []


def read_excel():
    wb = xlrd.open_workbook(filename=file)#打开文件
    print(wb.sheet_names())#获取所有表格名字

    sheet1 = wb.sheet_by_index(0)#通过索引获取表格
    print(sheet1.name,'   行数：', sheet1.nrows, '   列数：',sheet1.ncols)
    # 获取行数
    nrows = sheet1.nrows
    # 获取列数
    ncols = sheet1.ncols
    print ('nrows: ', nrows, ' ncols: ', ncols)

    # 获取各行数据
    for i in range(1, nrows):
        row_data = sheet1.row(i)[0].value
        row_list.append(row_data)

#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

#写Excel
def write_excel():
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('结果',cell_overwrite_ok=True)
    row0 = ["订单ID","物流"]
    #写第一行
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    #写数据
    for i in range(0, len(res_list)):
        sheet1.write(i+1, 0, row_list[i])
        sheet1.write(i+1, 1, res_list[i])
    f.save('orders_res.xls')

async def taobao_login(username, password, url):
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    :return: 登录cookies
    """
    # 'headless': False如果想要浏览器隐藏更改False为True
    browser = await launch({'headless': False,  'executablePath':'D:\ProgramFiles\Anaconda3\chrome\chrome.exe'}) #'args': ['--no-sandbox'],
    #browser.__setattr__() #最大化窗口
    #browser = await launch({'headless': False, 'args': ['--no-sandbox', '--proxy-server=socks5://127.0.0.1:1080']})
    page = await browser.newPage()
    # 设置页面视图大小
    await page.setViewport(viewport={'width': 1280, 'height': 800})
    # 是否启用JS，enabled设为False，则无渲染效果
    await page.setJavaScriptEnabled(enabled=True)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    await page.goto(url)

    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    await page.click('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
    page.mouse
    time.sleep(1)
    # 输入用户名，密码
    await page.type('#TPL_username_1', username, {'delay': input_time_random() - 50})   # delay是限制输入的时间
    await page.type('#TPL_password_1', password, {'delay': input_time_random()})
    time.sleep(2)
    # 检测页面是否有滑块。原理是检测页面元素。
    slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块

    if slider:
        print('当前页面出现滑块')
        # await page.screenshot({'path': './headless-login-slide.png'}) # 截图测试
        flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
        if flag:
            #await page.keyboard.press('Enter')  # 确保内容输入完毕，少数页面会自动完成按钮点击
            #print("print enter", flag)
            await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。
            time.sleep(2)
            cookies_list = await page.cookies()
            print(cookies_list)
            await get_cookie(page)  # 导出cookie 完成登陆后就可以拿着cookie玩各种各样的事情了。
    else:
        print("没有滑块")
        #await page.keyboard.press('Enter')
        #print("print enter")
        #await _evaluate(page)
        await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')
        await page.waitFor(20)
        await page.waitForNavigation()

        try:
            global error  # 检测是否是账号密码错误
            print("error_1:", error)
            error = await page.Jeval('.error', 'node => node.textContent')
            print("error_2:", error)
        except Exception as e:
            error = None
        finally:
            if error:
                print('确保账户安全重新入输入')
                # 程序退出。
                loop.close()
            else:
                print(page.url)
                #await _evaluate(page)
                await get_cookie(page)
    #return await get_cookie(page)
    await page.setRequestInterception(True)
    page.on('request', request_check)
    '''
    await asyncio.wait([
        page.click('a.my-link'),
        page.waitForNavigation(),
    ])
    '''
    await page.goto(URL_MYBAOBEI)
    await page.waitForSelector('.search-mod__order-search-input___29Ui1')
    await page.waitFor(20)
    await page.waitForSelector('.pagination-item')
    #await page.Jeval('.search-mod__order-search-input___29Ui1', 'node => node.val="dddd"')
    #await page.evaluate('''document.querySelector(".search-mod__order-search-button___1q3E0").click()''')
    #await page.evaluate(        '''document.querySelector(".search-mod__order-search-input___29Ui1").value="''' + ORDER_QUERY + '''"''')
    for i in range(0, len(row_list)):
        ORDER_QUERY = row_list[i]
        # 在搜索框中输入ORDER_QUERY
        await page.waitForSelector('input.search-mod__order-search-input___29Ui1')
        await page.evaluate(
            '''document.querySelector("input.search-mod__order-search-input___29Ui1").value=""''')
        await page.type('input.search-mod__order-search-input___29Ui1', ORDER_QUERY)
        # 点击搜索按钮
        await page.click('button.search-mod__order-search-button___1q3E0')
        # 滚动到页面底部
        await page.evaluate('window.scrollBy(0, window.innerHeight)')
        time.sleep(random.random() * 5)

        try:
            # 检测是否有物流信息
            #await page.waitForSelector('#viewLogistic')
            wuliuinfo = await page.J('#viewLogistic')  # 查看物流
            if wuliuinfo:
                print("查看物流")
                # await page.click('#viewLogistic') #会打开新窗口
                try:
                    await page.hover('#viewLogistic')  # 模拟鼠标划 查看物流 加载出物流信息
                    # await asyncio.sleep(2)
                    await page.waitFor(20)
                    await page.waitForSelector('.logistics-info-mod__header___r5tzb')
                    wuliustatInfo1 = await page.evaluate(
                        '''document.querySelector(".logistics-info-mod__header___r5tzb span:nth-child(1)").innerHTML''')
                    wuliustatInfo2 = await page.evaluate(
                        '''document.querySelector(".logistics-info-mod__header___r5tzb span:nth-child(2)").innerHTML''')
                    wuliustatInfo3 = await page.evaluate(
                        '''document.querySelector(".logistics-info-mod__header___r5tzb span:nth-child(3)").innerHTML''')
                    wuliustatInfo = wuliustatInfo1 + wuliustatInfo2 + wuliustatInfo3
                    print(wuliustatInfo)
                    res_list.append(wuliustatInfo)
                    # wuliustatInfoHtml = await page.Jeval('.logistics-info-mod__header___r5tzb', 'node => node.innerHTML')

                except Exception as e:
                    print(e, ':查看物流信息失败')
                    res_list.append('无')
            else:
                print("没有查看物流")
                res_list.append('无')
        except Exception as e:
            print(e, ':异常没有查看物流')
            res_list.append('无')

    return await browser.close()

async def request_check(req):
    '''请求过滤'''
    if req.resourceType in ['image', 'media', 'eventsource', 'websocket']:
        await req.abort()
    else:
        await req.continue_()



async def _evaluate(page, retries=0):
    if retries > 10:
        return await page.evaluate('document.body.innerHTML')
    else:
        try:
            return await page.evaluate('document.body.innerHTML')
        except pyppeteer.errors.NetworkError:
             await asyncio.sleep(0.5)
             return await _evaluate(page, retries+1)
# 获取登录后cookie
async def get_cookie(page):
    # res = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    # print(cookies)
    return cookies


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none)
async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        if slider_again != '验证通过':
            return None, page
        else:
            # await page.screenshot({'path': './headless-slide-result.png'}) # 截图测试
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)



if __name__ == '__main__':
    username = USER_NAME
    password = USER_PASSWORD
    url = URL_LOGIN2
    read_excel()
    asyncio.get_event_loop().run_until_complete(taobao_login(username, password, url))
    write_excel()
    '''
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(taobao_login(username, password, url))
    loop.run_until_complete(task)
    cookie = task.result()
    print(cookie)
    '''
