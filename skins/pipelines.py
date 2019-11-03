# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class SkinsPipeline(object):
    def open_spider(self, spider):
        self.file = open('out.csv', 'a', encoding='utf-8', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow((spider.name, ""))

    def process_item(self, item, spider):
        self.writer.writerow((item['name'], item['price']))
        return item

    def close_spider(self, spider):
        self.file.close()
