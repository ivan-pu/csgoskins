from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from skins.spiders.buff import BuffSpider

import os
import logging
import sys


def runspider(ch,en):
    process = CrawlerProcess(get_project_settings())
    try:

        process.crawl('c5', tag=ch)
        process.crawl('bitskins', tag=en)
        process.crawl('buff', tag=ch)
        process.start()
    except Exception as e:
        print('exception:%s' % e)

runspider('蝴蝶','butterfly')
