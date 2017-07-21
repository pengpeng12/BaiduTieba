# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random

import requests


class BaidutiebaSpiderMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        result = requests.get('http://dev.kuaidaili.com/api/getproxy?orderid=949187989849476&num=100&kps=1')
        if result.status_code==200:
            self.ipList = result.text.split('\n')
            # print(self.ipList)

    def get_rand_ip(self):
        # 代理ip
        rand = random.randint(0, len(self.ipList) - 1)
        dlIp = self.ipList[rand]
        self.logger.debug('Using ip------' + dlIp)
        return "http://" + dlIp

    def process_request(self, request, spider):
        # request.meta['proxy'] = self.get_rand_ip()
        pass