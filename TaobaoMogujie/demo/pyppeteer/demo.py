import asyncio
from pyppeteer import launch



async def screenshot():
    browser = await launch()
    # 取消默认下载chromium的行为 加环境变量PUPPETEER_SKIP_CHROMIUM_DOWNLOAD 并增加 executablePath 参数
    #browser = await launch({'headless': False, 'args': ['--no-sandbox'], 'executablePath': 'D:\ProgramFiles\Anaconda3\chrome\chrome.exe'})
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()

async def evaluate_script():
    browser = await launch(
        {'headless': False, 'args': ['--no-sandbox'], 'executablePath': 'D:\ProgramFiles\Anaconda3\chrome\chrome.exe'})
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()

async def main():
    #await evaluate_script()
    await screenshot()

asyncio.get_event_loop().run_until_complete(main())