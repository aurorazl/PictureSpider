from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
import redis

from scrapy_redis.dupefilter import RFPDupeFilter
from scrapy_redis.connection import get_redis_from_settings
from scrapy_redis import defaults

class RepeatFilter(BaseDupeFilter):

    def __init__(self):
        self.visited_url = set()

    @classmethod        #不用创建对象执行该方法，内部通过obj = RepeatFilter.from_settings()先执行该方法
    def from_settings(cls, settings):
        # print('.............')
        return cls()        #cls是当前类名，cls()返回对象,即调用类的构造方法，init()，用途是创建对象

    def request_seen(self, request):
        request_url = request_fingerprint(request)
        if request_url in self.visited_url:     # 能连接数据库，redis
            return True
        self.visited_url.add(request_url)
        return False

    def open(self):  # can return deferred  # 爬虫开始时
        # print('open')
        pass

    def close(self, reason):  # can return a deferred
        # print('close')
        pass

    def log(self, request, spider):  # log that a request has been filtered
        pass
