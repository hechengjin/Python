import requests
import bs4
import chardet
import logging.handlers
import os
import urllib
import sys
import time

def get_video_page_urls():

    #urllib
    # response = GetHtml(url);
    # soup = bs4.BeautifulSoup(response)
    #request
    response = requests.get(url)
    # response.text There will be random code in Chinese
    soup = bs4.BeautifulSoup(response.content)
    sortNum =0
    for a in soup.select('div.CM-video-list-three li a[node-type]'):
        sortNum +=1;
        curTime = str(time.time()).replace('.', '')+ '0'
        logger.debug("INSERT INTO comm_record_test(class_id,sort_num,title,label,relative_path,file_size,file_type,content_html,content_plain,status,modify_time,create_time) VALUES (10," + str(sortNum) +",'"+ a.text + "','','" + a.attrs.get('href') +"',1000,'WEB','','',0,"+curTime+","+curTime+")")

def GetHtml( url):
    page = urllib.urlopen(url)
    contex = page.read()
    return contex

if __name__ == '__main__':
    url = "http://tech.sina.com.cn/zt_d/blockchain_100/"
    logFileName = "blockchain";
    logFilePath = os.path.abspath(os.curdir) + "/";
    print sys.getfilesystemencoding()
    print 'Html is encoding by : %', chardet.detect(GetHtml(url))
    if not os.path.exists(logFilePath):
        os.makedirs(logFilePath)
    logger = logging.getLogger(logFileName + '_log')
    logger.setLevel(logging.DEBUG)
    rh = logging.handlers.RotatingFileHandler(logFilePath + logFileName + '.log', maxBytes=50 * 1024 * 1024, backupCount=20)
    formatter = logging.Formatter('%(asctime)s - %(name)s - V2 API - %(levelname)s - %(message)s')
    rh.setFormatter(formatter)
    logger.addHandler(rh)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)

    get_video_page_urls()