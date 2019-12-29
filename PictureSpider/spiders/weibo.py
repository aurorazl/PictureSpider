# -*- coding: utf-8 -*-
import scrapy
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

def get_cookie_from_login_sina_com_cn(account, password):
    """ 获取一个账号的Cookie """
    loginURL = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode("gbk")
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print("Get Cookie Success!( Account:%s )" % account)
        cookie = session.cookies.get_dict()
        return cookie
    else:
        print("Failed!( Reason:%s )" % info["reason"])
        return

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['s.weibo.com']
    start_urls = ['http://s.weibo.com/']
    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,ko;q=0.7',
        'Cache-Control': 'max-age=0',
        "Connection": "keep - alive",
        "Host": "s.weibo.com",
        "Upgrade-Insecure-Requests":1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    # cookie = "_s_tentry=gl.ali213.net; UOR=gl.ali213.net,widget.weibo.com,www.howtoing.com; login_sid_t=99adeb40c85314559f6ee27d85c6f289; cross_origin_proto=SSL; Apache=425584148259.2815.1577595064696; SINAGLOBAL=425584148259.2815.1577595064696; ULV=1577595064704:1:1:1:425584148259.2815.1577595064696:; un=dragon0486@163.com; wvr=6; SCF=AguUrz2aOzj6aiKJhuVtR80rMWc5WaBk4DEu4fA0ueqo9Y-vfiCWNcQjcQHuVcDllLZoD9v6STIkNOfyXywxBG0.; SUB=_2A25zDCIjDeRhGeRG71IR8ifPyj6IHXVQeBTrrDV8PUNbmtAfLVX5kW9NUgurfxRxnfnunDO6Gt0_GUSu_R96wOES; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhYmq3C-xkW9MRrIH1nbCWm5JpX5K2hUgL.FozRSh57eo.0eKz2dJLoIpjLxK-L1KeL1h2LxK-LBonL12eLxKBLBonLBoqt; SUHB=0h1Irx3w-2C_Rv; ALF=1609139699; SSOLoginState=1577603699; secsys_id=2ce88653d2afbc8451f64cc14476bd09; WBStorage=42212210b087ca50|undefined; webim_unReadCount=%7B%22time%22%3A1577607574098%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D"
    # cookie = stringToDict(cookie)
    main_keyword = ['军人', '城市工人', '警察', '工人', '施工', '站岗', '洪水', '抢修', '军训', '工地', '洪涝', '电力', "教官"]
    second_keyword = ['冬季', '冬天', '夜间', '水利', '暴雨', '参观', '遮阳帽', '变电站', '绒毛帽', '雨天', '鸭舌帽', '旅游', '雪地', '毛帽', '南网',
                      '草帽', '雷雨',
                      '棒球帽', '严寒', '鹅毛大雪', '照明']
    total_keyword = []
    for i in main_keyword:
        total_keyword.append(i)
        for j in second_keyword:
            total_keyword.append(i + " " + j)

    cookie = get_cookie_from_login_sina_com_cn("dragon0486@163.com","long0486.")
    if not cookie:
        logging.error("\nuser login fail,existing!!\n")
        exit(0)

    def start_requests(self):
        for one in self.total_keyword:
            crawl_url = "https://s.weibo.com/weibo?q="+ one+ "&nodup=1&page=1"
            yield Request(url=crawl_url, callback=self.parse,cookies=self.cookie,headers=self.default_headers)

    def parse(self, response):
        id_list = Selector(response=response).xpath('//div[@class="media media-piclist"]//img[re:test(@src,"\S+\.jpg")]/@src').extract()
        for url in id_list:
            url_path = "https://wx3.sinaimg.cn/large/{}".format(url.split("/")[-1])
            item_obj = BingItem(href=url_path, save_prefix="helmet_weibo")
            yield item_obj

        id_list = Selector(response=response).xpath('//div[@class="m-page"]//a[@class="next"]/@href').extract()
        for next_url in id_list:
            if int(next_url.split("&page=")[-1])>int(response.url.split("&page=")[-1]): # 最多50页
                logging.info(next_url)
                yield Request(url="https://s.weibo.com"+next_url, callback=self.parse,
                              headers=self.default_headers.update({"Referer":response.url}),
                              cookies=self.cookie,meta={
                                'dont_redirect': True,
                                'handle_httpstatus_list': [302]
                                },)

