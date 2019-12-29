# -*- coding: utf-8 -*-
import scrapy
import re
import base64
from scrapy.http import Request
from scrapy.selector import Selector
from PictureSpider.logger import set_logger
import requests
import json
import logging
from PictureSpider.items import BingItem
set_logger("weibo", logging.INFO)

def stringToDict(cookie):
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict

class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/']
    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,ko;q=0.7',
        'Cache-Control': 'max-age=0',
        "Connection": "keep - alive",
        "Host": "weibo.com",
        "Upgrade-Insecure-Requests": 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    total_uids = [3774270292]
    cookie = "SUB=_2AkMpVAVSf8NxqwJRmP0Rz2rkbotxyADEieKfCPSJJRMxHRl-yT92qhM-tRB6AtQrvY08cq5f0eqJBjDNWWXmefbHUgRU; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhlC33DKKO.YC2nM-YjWZPF; _s_tentry=passport.weibo.com; Apache=761105768858.8341.1577618022675; SINAGLOBAL=761105768858.8341.1577618022675; ULV=1577618022724:1:1:1:761105768858.8341.1577618022675:; YF-Page-G0=135ed72e4454a508b0f28ef4384e19b1|1577618031|1577618017"
    cookie = stringToDict(cookie)

    def start_requests(self):
        for one in self.total_uids:
            crawl_url = "https://weibo.com/u/{}?is_search=0&visible=0&is_pic=1&is_tag=0&profile_ftype=1&page=1#feedtop".format(one)
            yield Request(url=crawl_url, callback=self.parse,headers=self.default_headers,cookies=self.cookie)

    def parse(self, response):
        pic_content = re.findall(r'<img src=\\"(.*?)\\"\sstyle=.*?>', response.text, re.S)
        # for url in pic_content:
        #     url_path = "https://ww1.sinaimg.cn/large/{}".format(url.replace("\\","").split("/")[-1])
        #     item_obj = BingItem(href=url_path, save_prefix="helmet_sina")
        #     yield item_obj

        logging.info(response.text)# 翻页
        next_content = re.findall(r'<.*?page.*?>', response.text, re.S)
        print(next_content)
