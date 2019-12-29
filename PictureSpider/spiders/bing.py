# -*- coding: utf-8 -*-
import scrapy
import sys
import io
import re
import logging
import json
import os
from scrapy.http import Request
from scrapy.selector import Selector
from PictureSpider.logger import set_logger
from PictureSpider.items import BingItem
set_logger("bing", logging.INFO)

current_index=0
max_num = 1000
class BingSpider(scrapy.Spider):
    name = 'bing'
    allowed_domains = ['cn.bing.com']
    start_urls = ['https://cn.bing.com/']
    main_keyword = ['军人', '城市工人', '警察', '工人', '施工', '站岗', '洪水', '抢修', '军训', '工地', '洪涝', '电力', "教官"]
    second_keyword = ['冬季', '冬天', '夜间', '水利', '暴雨', '参观', '遮阳帽', '变电站', '绒毛帽', '雨天', '鸭舌帽', '旅游', '雪地', '毛帽', '南网',
                      '草帽', '雷雨',
                      '棒球帽', '严寒', '鹅毛大雪', '照明']
    default_headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,ko;q=0.7',
        # 'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    total_keyword = []
    for i in main_keyword:
        total_keyword.append(i)
        for j in second_keyword:
            total_keyword.append(i + " " + j)

    def start_requests(self):
        for one in self.total_keyword:
            crawl_url = "https://cn.bing.com/images/async?q="+one+"&first=0&count=60&relp=60&lostate=r&mmasync=1"
            yield Request(url=crawl_url, callback=self.parse,headers=self.default_headers)

    def parse(self, response):
        id_list = Selector(response=response).xpath('//div[@class="imgpt"]/a/@m').extract()
        for one in id_list:
            item_obj = BingItem(href=json.loads(one).get("murl"), save_prefix="helmet_bing")
            yield item_obj

        # global current_index
        # current_index += 60
        # if current_index<max_num:
        #     for one in self.total_keyword:
        #         crawl_url = "https://cn.bing.com/images/async?q=" + one + "&first={}&count={}&relp=60&lostate=r&mmasync=1".format(current_index,current_index+60)
        #         yield Request(url=crawl_url, callback=self.parse, headers=self.default_headers)
