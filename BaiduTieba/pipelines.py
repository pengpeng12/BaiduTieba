# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

import MySQLdb

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# import pymysql

from BaiduTieba.items import BaidutiebaItem


class BaidutiebaPipeline(object):
    def __init__(self, mysql_uri, mysql_db, mysql_user, mysql_password, mysql_port, mysql_charset):
        self.mysql_uri = mysql_uri
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_port = mysql_port
        self.mysql_charset = mysql_charset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_URI'),
            mysql_db=crawler.settings.get('MYSQL_DATABASE'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_charset=crawler.settings.get('MYSQL_CHARSET')
        )

    def open_spider(self, spider):
        # self.conn = pymysql.connect(host=self.mysql_uri, port=self.mysql_port, user=self.mysql_user,
        #                             passwd=self.mysql_password, db=self.mysql_db, charset=self.mysql_charset)
        self.conn = MySQLdb.connect(host=self.mysql_uri, port=self.mysql_port, user=self.mysql_user,
                                    passwd=self.mysql_password, db=self.mysql_db, charset=self.mysql_charset)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, BaidutiebaItem):
            data = (
                item.get('vc_date'), item.get('vc_keyWord'), item.get('vc_baName'), item.get('vc_baUrl'),
                item.get('vc_label'), item.get('vc_contents'), item.get('vc_summary'), item.get('vc_peopleNum'),
                item.get('vc_tieNum')
            )
            try:
                self.cur.callproc('pro_add_tieba_search', data)
                self.conn.commit()
                # print 'pro_add_tieba_search成功插入 ', self.cur.rowcount, '条数据'
                print('pro_add_tieba_search成功插入 ', self.cur.rowcount, '条数据')
                return item
            # except Exception, r:
            #     logging.error(msg="{}:{},{}".format(Exception, r, 'pro_add_tieba_search'))
            except Exception as r:
                print(r)
