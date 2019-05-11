import requests
#https://2.python-requests.org/en/master/
#https://www.runoob.com/python3/python3-tutorial.html
def testGet():
    response = requests.get('https://www.baidu.com')
    print(type(response))
    print(response.status_code)
    print(type(response.text))
    print(response.cookies)
def testPost():
    requests.post('http://httpbin.org/post')
    requests.put('http://httpbin.org/put')
    requests.delete('http://httpbin.org/delete')
    requests.head('http://httpbin.org/get')
    requests.options('http://httpbin.org/get')

testGet()
testPost()