# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy import Spider, Request

from BaiduTieba.items import BaidutiebaItem
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class TiebaSpider(Spider):
    name = "tieba"
    download_delay = 1
    allowed_domains = ["tieba.baidu.com"]
    start_url = 'http://tieba.baidu.com/f/index/forumclass'
    # start_urls = ['http://tieba.baidu.com/f/index/forumpark?cn=%E6%B8%AF%E5%8F%B0%E4%B8%9C%E5%8D%97%E4%BA%9A%E6%98%8E%E6%98%9F&ci=0&pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&st=new']
    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse_index)

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield Request(url=url, callback=self.parse_start)
    def parse_index(self, response):
        if response.status == 200:
            keyword_urlLi = response.xpath('//div[@class="class-item"]')
            for keywordUrl in keyword_urlLi:
                # if i == 0:
                keyword = keywordUrl.xpath('./a[@class="class-item-title"]/text()').extract_first()
                # print(keyword)
                labelLi = keywordUrl.xpath('./ul/li/a/text()').extract()
                # print(labelLi)
                for label in labelLi:
                    # if i == 0:
                    #st=new---人气最热
                    #st=popular---最近流行
                    #&pn=2---页数
                    newlabelUrl = 'http://tieba.baidu.com/f/index/forumpark?cn={label}&ci=0&pcn={keyword}pci=0&ct=1&st=new'.format(label=label,keyword=keyword)
                    newrequest = Request(url=newlabelUrl,callback=self.parse_totalPage)
                    newrequest.meta['vc_keyWord'] = keyword
                    newrequest.meta['vc_label'] = label
                    newrequest.meta['vc_contents'] = '人气最热'
                    yield newrequest

                    popularlabelUrl = 'http://tieba.baidu.com/f/index/forumpark?cn={label}&ci=0&pcn={keyword}pci=0&ct=1&st=popular'.format(
                        label=label, keyword=keyword)
                    popularlabelUrl = Request(url=popularlabelUrl, callback=self.parse_totalPage)
                    popularlabelUrl.meta['vc_keyWord'] = keyword
                    popularlabelUrl.meta['vc_label'] = label
                    popularlabelUrl.meta['vc_contents'] = '最近流行'
                    yield popularlabelUrl

    def parse_totalPage(self, response):
        if response.status == 200:
            totalPage = response.xpath('//a[@class="last"]/@href').extract_first()
            rp = re.compile('(?<=pn=)\d+')
            presult = rp.search(totalPage)
            if presult:
                totalPage = presult.group(0)
            else:
                totalPage = 1
            # print('totalPage==', totalPage)
            pageString = '&pn={}'
            for page in range(0,int(totalPage)):
                # if page == 1:
                labelUrl = response.url + pageString.format(page+1)
                request = Request(url=labelUrl, callback=self.parse_start)
                request.meta['vc_keyWord'] = response.meta['vc_keyWord']
                request.meta['vc_label'] = response.meta['vc_label']
                request.meta['vc_contents'] = response.meta['vc_contents']
                yield request


    def parse_start(self, response):
        if response.status == 200:
            v_keyWord = response.meta['vc_keyWord']
            v_label = response.meta['vc_label']
            v_contents = response.meta['vc_contents']
            ba_infoLi = response.xpath('//div[@id="ba_list"]/div')
            # print('ba_infoLicount==',len(ba_infoLi))
            for bainfo in ba_infoLi:
                v_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                v_baName = bainfo.xpath('.//p[@class="ba_name"]/text()').extract_first()
                v_baUrl = 'http://tieba.baidu.com' + bainfo.xpath('./a[@class="ba_href clearfix"]/@href').extract_first()
                v_peopleNum = bainfo.xpath('.//span[@class="ba_m_num"]/text()').extract_first()
                v_tieNum = bainfo.xpath('.//span[@class="ba_p_num"]/text()').extract_first()
                v_summary = bainfo.xpath('.//p[@class="ba_desc"]/text()').extract_first()
                # print(v_baName,v_baUrl,v_peopleNum,v_tieNum,v_summary)

                vc_date = v_date
                vc_keyWord = v_keyWord
                vc_label = v_label
                vc_contents = v_contents
                vc_baName = v_baName
                vc_baUrl = v_baUrl
                vc_summary = v_summary
                vc_peopleNum = v_peopleNum
                vc_tieNum = v_tieNum

                item = BaidutiebaItem()
                for field in item.fields:
                    try:
                        item[field] = eval(field)
                    except NameError:
                        pass
                yield item
