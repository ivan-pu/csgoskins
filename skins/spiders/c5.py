# -*- coding: utf-8 -*-
import scrapy
from skins.items import SkinsItem
from scrapy.exceptions import CloseSpider


class C5Spider(scrapy.Spider):
    name = 'c5'
    allowed_domains = ['www.c5game.com']

    def start_requests(self):
        url = 'https://www.c5game.com/csgo/default/result.html?min=&max=&k='
        tag = getattr(self, 'tag', None)
        if not tag: raise CloseSpider('search tag not detected')
        tag = tag.split("#")
        for t in tag:
            url += t + "+"
        url = url[:-1]+'&sort=price'
        req = scrapy.Request(url, callback=self.parse)
        yield req


    def parse(self, response):
        print("saving......")
        item = SkinsItem()
        count = 0
        for list in response.css('div.active li.selling'):
            if count > 10: break
            item['name'] = list.css('p.name a span::text').get()
            item['price'] = list.css('p.info span.price::text').get()
            count += 1
            yield item
