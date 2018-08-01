import os
import sys
import time

from bs4 import BeautifulSoup
import codecs
import urllib
import urllib.request

# from selenium import webdriver

def analysis_html(soup_html):
    title = soup_html.find('h1', {'class': 'title mathjax'}).contents[1].strip()
    href = soup_html.find('a', {'accesskey': 'f'})["href"]
    version = href[href.rfind('/')+1:]
    return title, version

def save_download(list1, pathname_download):
    content = ""
    for item in list1:
        content = content + "http://cn.arxiv.org/pdf/{0}\n".format(item['version'])
        content = content + "  out={0}.pdf\n".format(item['version'])
        content = content + "  dir=arxiv\n"
    with codecs.open(pathname_download, 'w', encoding='utf-8') as f:
        f.write(content) 

def save_md(list1, pathname_md):
    content = ""
    content = content + "\n# {0}\n".format("arxiv")
    content = content + "\n|#|id|title|note|\n"
    content = content + "|-|-|-|-|\n"
    for i, item in enumerate(list1):
        url_abs = 'http://cn.arxiv.org/abs/{0}'.format(item['id'])
        content = content + "|{0}|[{1}]({2})|{3}|{4}|\n".format(i + 1, item['id'], url_abs, item['title'], item['note'])
    with codecs.open(pathname_md, 'w', encoding='utf-8') as f:
        f.write(content) 

def process(infos):
    list1 = []
    # driver = webdriver.Chrome()    
    for i in range(len(infos) // 2):
        id = infos[i*2]
        note = infos[i*2 + 1]
        print(i, id)
        url_abs = 'http://cn.arxiv.org/abs/{0}'.format(id)
        html=urllib.request.urlopen(url_abs).read()
        soup_html = BeautifulSoup(html, features='lxml')
        # driver.get(url_abs)        
        # soup_html = BeautifulSoup(driver.page_source, features='lxml')
        title, version = analysis_html(soup_html)
        list1.append({'id': id, 'title':title, 'version': version, 'note': note})
    # driver.close()

    save_download(list1, 'arxiv_download.txt')
    save_md(list1, "arxiv.md")

def main(argv):
    infos = [
        '1312.2249', '',
        '1409.1556', '',
        '1409.4842', '',
        '1502.03167', '',
        '1503.03832', 'facenet',
        '1512.00567', '',
        '1512.03385', '',
        '1601.06759', '',
        '1602.07261', '',
        '1603.05027', '',
        '1604.02878', 'mtcnn',
        '1609.03605', '',
        '1611.02200', '',
        '1703.10593', '',
        '1704.02470', '',
        '1704.03549', 'attention-ocr',
        '1704.04861', '',
        '1706.03059', '',
        '1706.03762', '',
        '1706.05137', '',
        '1707.07012', '',
        '1708.05509', '',
        '1708.02002', 'RetinaNet',
        '1710.10196', '',
        '1712.00559', '',
        '1801.04381', '',
        '1801.09797', '',
        '1801.10198', '',
        '1802.02611', '',
        '1802.05751', '',
        '1803.02155', '',
        '1803.03382', '',
        '1803.07416', 'tensor2tensor',
        '1804.00247', '',
        '1804.04235', '',
    ]
    process(infos)

if __name__ == '__main__':
    main(sys.argv)
