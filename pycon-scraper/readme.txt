在抓取网站中有两个基本的任务：
1.加载网页到一个 string 里。
2.从网页中解析 HTML 来定位感兴趣的位置。
Python 为上面两个任务提供了两个超棒的工具。我将使用 requests 去加载网页，用 BeautifulSoup 去做解析。


爬虫翻墙
但是如果我们直接运行上面那段最终代码的话是妥妥的会超时报错的。原因你肯定知道，就是不可逾越的长城。一般 Pyvideo.org 是能上去，但是 YouTube 被墙了。所以这里就需要代理出马了。最简单的可以安装 GoAgent 。在本地运行 GoAgent 后，使用 requests.get() 的 proxies 参数，将代理设置成本地的 127.0.0.1 端口为 8087 ，爬虫就能够通过代理访问网页了。使用的代码如下：

proxy = {"http":"http://127.0.0.1:8087","https":"https://127.0.0.1:8087"}
response = requests.get(video_data['youtube_url'],proxies = proxy,verify=False)
将最终版本的代码的第22行response = requests.get(video_data['youtube_url'])替换成上面的代码即可。如果 Pyvideo.org 也上不了（校园网有时候就是这么抽风），就把 proxy 设成全局的，在所有调用 requests.get() 的地方设置 proxies 参数即可。

你可能会疑惑 verify 参数是干嘛的。这是对 HTTPS 请求做 SSL 验证的（YouTube 是 HTTPS 连接）。调用requests.get()的时候默认verify参数为True，就是会进行验证。如果我们通过代理爬取站点，SSL 验证一般是不会通过的，会返回 [SSL: CERTIFICATE_VERIFY_FAILED] 错误。所以需要将verify关闭。

https://blog.csdn.net/u011279649/article/details/52790479


日志文件输出
https://www.cnblogs.com/arkenstone/p/5727883.html