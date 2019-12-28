# coding=utf-8
"""根据搜索词下载百度图片"""
import re
import sys
import urllib.parse
import hashlib
import requests
import os

def getPage(keyword, page, n):
    page = page * n
    keyword = urllib.parse.quote(keyword, safe='/')
    url_begin = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="
    url = url_begin + keyword + "&pn=" + str(page) + "&gsm=" + str(hex(page)) + "&ct=&ic=0&lm=-1&width=0&height=0"
    return url

def get_onepage_urls(onepageurl):
    try:
        html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []
        return pic_urls
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    return pic_urls


def down_pic(pic_urls):
    """给出图片链接列表, 下载所有图片"""
    for pic_url in pic_urls:
        try:
            pic = requests.get(pic_url, timeout=15)
            sha1 = hashlib.sha1()
            sha1.update(pic_url.encode('utf-8'))
            hashcode = sha1.hexdigest()
            global total_number,fail_number
            if os.path.exists(os.path.join("images",hashcode+".jpg")):
                continue
            with open(os.path.join("images",hashcode+".jpg"), 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (total_number, str(pic_url)))
                total_number+=1
        except Exception as e:
            print('下载图片第%s次失败: %s' % (str(fail_number), str(pic_url)))
            fail_number += 1
            print(e)
            continue


if __name__ == '__main__':
    total_number = 0
    fail_number = 0
    page_begin = 0
    page_number = 30
    image_number = 3
    all_keyword = ["洪涝 抢修","洪涝 电力","暴雨 电力","夜间 抢修","南网 夜间","南网 抢修",
        "南网 雪地","南网 冬季","遮阳帽 电力","遮阳帽 施工","遮阳帽 工地","遮阳帽 工人","照明 施工",
        "照明 工地","工地 夜间 照明","参观 施工","参观 夜间 施工","水利 施工","变电站 维修","鸭舌帽 冬天",
        "绒毛帽 城市工人","草帽 城市工人","鸭舌帽 雨天","草帽 旅游","鸭舌帽 旅游","军训 教官","军人 雪地",
                   "夜间 施工","雷雨 施工","警察 鹅毛大雪","警察 严寒","警察 站岗 雪地","棒球帽 雨天","毛帽 工人",
                   "雷雨 抢修","洪水 抢修","洪水 电力"
    ]
    while 1:
        for keyword in all_keyword:
            url = getPage(keyword, page_begin, page_number)
            onepage_urls = get_onepage_urls(url)
            down_pic(onepage_urls)
        page_begin += 1
        print("the {} times".format(page_begin))
