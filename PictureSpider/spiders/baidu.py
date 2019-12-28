# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.http.cookies import CookieJar
from scrapy.selector import Selector
import sys
import io
import re
import logging
import os
from PictureSpider.items import BaiduItem
from scrapy.utils.project import get_project_settings
from PictureSpider.logger import set_logger

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

Index = 0
Total_num = 50000
set_logger("baidu", logging.INFO)

def get_image_number():
    img_store = get_project_settings().get('IMAGES_STORE')
    if not os.path.exists(img_store + "/" + "helmet"):
        os.makedirs(img_store + "/" + "helmet",exist_ok=True)
    return len(os.listdir(img_store + "/" + "helmet"))

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['image.baidu.com']
    url_begin = "https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="
    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }
    all_keyword = ["洪涝 抢修", "洪涝 电力", "暴雨 电力", "夜间 抢修", "南网 夜间", "南网 抢修",
                   "南网 雪地", "南网 冬季", "遮阳帽 电力", "遮阳帽 施工", "遮阳帽 工地", "遮阳帽 工人", "照明 施工",
                   "照明 工地", "工地 夜间 照明", "参观 施工", "参观 夜间 施工", "水利 施工", "变电站 维修", "鸭舌帽 冬天",
                   "绒毛帽 城市工人", "草帽 城市工人", "鸭舌帽 雨天", "草帽 旅游", "鸭舌帽 旅游", "军训 教官", "军人 雪地",
                   "夜间 施工", "雷雨 施工", "警察 鹅毛大雪", "警察 严寒", "警察 站岗 雪地", "棒球帽 雨天", "毛帽 工人",
                   "雷雨 抢修", "洪水 抢修", "洪水 电力"
                   ]
    def start_requests(self):
        for one in self.all_keyword:
            crawl_url = self.url_begin +one+ "&pn=" + str(1) + "&gsm=" + str(hex(1)) + \
                        "&ct=&ic=0&lm=-1&width=0&height=0"
            yield Request(url=crawl_url, callback=self.parse,headers=self.default_headers)

    def parse(self, response):
        global Index
        pic_content = re.findall('{.*?"objURL":\s*"(.*?)",.*?"fromPageTitle":\s*"(.*?)".*?}',response.text,re.S)
        for url,title in pic_content:
            item_obj = BaiduItem(title=str(Index),href=url,save_prefix="helmet")
            Index +=1
            if get_image_number() > Total_num:
                break
            yield item_obj

        if Total_num < Total_num:
            id_list = Selector(response=response).xpath('//div[@id="page"]/a/@href').extract()
            if not id_list:
                logging.info("==================== not id_list\n")
            for one in id_list:
                if get_image_number()>Total_num:
                    break
                logging.info("begin crawl page: {}".format("https://image.baidu.com" + one))
                yield Request(url="https://image.baidu.com" + one, callback=self.parse, headers=self.default_headers)

