# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BaidutiebaItem(Item):
    vc_date = Field()
    #关键字
    vc_keyWord = Field()
    # 标签
    vc_label = Field()
    # 目录（人气最热，最近流行）
    vc_contents = Field()
    vc_baName = Field()
    vc_baUrl = Field()
    #简介
    vc_summary = Field()
    #关注人数
    vc_peopleNum = Field()
    #吧内帖子数
    vc_tieNum = Field()
