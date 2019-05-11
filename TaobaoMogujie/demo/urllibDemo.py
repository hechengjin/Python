import urllib.request
import urllib.parse
import socket
import urllib.error
#https://docs.python.org/3/library/urllib.html

#get方法测试
def testGet():
    response = urllib.request.urlopen('http://www.baidu.com')
    print(response.read().decode('utf-8'))
def testPost():
    data = bytes(urllib.parse.urlencode({'word':'hello'}), encoding='utf8')
    response = urllib.request.urlopen('http://httpbin.org/post', data=data)
    print(response.read())
def testTime1():
    response = urllib.request.urlopen('http://httpbin.org/get', timeout=1)
    print(response.read())
def testTime2():
    try:
        response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print('TIME OUT')
testTime2()
#testTime1()
#testPost()
#testGet()