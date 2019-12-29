# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
import shutil
import hashlib
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import to_bytes

class PicturespiderPipeline(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }
    def get_media_requests(self, item, info):
        img_url = item['href']
        yield  scrapy.Request(img_url, headers=self.default_headers,meta={'item': item,})

    # def item_completed(self, results, item, info):
    #     image_path = [x['path'] for ok, x in results if ok]  # ok判断是否下载成功
    #     if not image_path:
    #         # raise DropItem("Item contains no images")
    #         return
    #     img_path = self.img_store+"/"+item['save_prefix']
    #     if not os.path.exists(img_path):
    #         os.makedirs(img_path,True)
    #     if not os.path.exists(self.img_store+"/"+image_path[0]):
    #         return
    #     shutil.move(self.img_store+"/"+image_path[0],img_path+"/"+image_path[0].split("/")[-1])
    #     return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return '{}/{}.jpg'.format(item["save_prefix"],image_guid)

class Pipeline(object):
    def process_item(self, item, spider):
        pass
