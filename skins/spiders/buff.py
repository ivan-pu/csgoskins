# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.exceptions import CloseSpider
from skins.items import SkinsItem


class BuffSpider(scrapy.Spider):
    name = 'buff'
    allowed_domains = ['buff.163.com']

    def start_requests(self):
        url = 'https://buff.163.com/market/?game=csgo#tab=selling&page_num=1&search='
        tag = getattr(self, 'tag', None)
        if not tag: raise CloseSpider('search tag not detected')
        tags = tag.split("#")
        for t in tags:
            url += t + " "
        url += '&sort_by=price.asc'
        req = scrapy.Request(url, callback=self.parse)
        yield req

    def parse(self, response):
        print("saving......")
        count = 0
        item = SkinsItem()
        for list in response.css('ul.card_csgo li'):
            if count > 10: break
            item['name'] = list.css('h3 a::text').get()
            item['price'] = list.css('p strong::text').get()
            if list.css('p strong small::text'):
                item['price'] += list.css('p strong small::text').get()
            count += 1
            yield item

    def closed(self, reason):
        print("closing.............")
        with open('out.csv', encoding='utf-8') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            res = []
            for row in readCSV:
                name = row[0]
                price = ''
                if row[1]:
                    price = row[1]
                res.append((name, price))
            print(res)
    # def parse_item(self, response):
    #     item = {}
    #     # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     # item['name'] = response.xpath('//div[@id="name"]').get()
    #     # item['description'] = response.xpath('//div[@id="description"]').get()
    #     return item
