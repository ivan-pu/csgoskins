# -*- coding: utf-8 -*-
import scrapy
from skins.items import SkinsItem
from scrapy.exceptions import CloseSpider


class BitskinsSpider(scrapy.Spider):
    name = 'bitskins'
    allowed_domains = ['www.bitskins.com']

    def start_requests(self):
        url = 'https://www.bitskins.com/?market_hash_name='
        tag = getattr(self, 'tag', None)
        if not tag: raise CloseSpider('search tag not detected')
        tag = tag.split("#")
        for t in tag:
            url += t + "+"
        url = url[:-1]+'&sort_by=price&order=asc'
        req = scrapy.Request(url, callback=self.parse)
        yield req


    def parse(self, response):
        print("saving......")
        item = SkinsItem()
        count = 0
        for list in response.css('div.item-solo'):
            if count > 10: break
            item['name'] = list.css('div.item-title::text').get()
            item['price'] = list.css('span.item-price::text').get()
            count += 1
            yield item
        # with open('res.html', 'wb') as res:
        #     res.write(response.body)