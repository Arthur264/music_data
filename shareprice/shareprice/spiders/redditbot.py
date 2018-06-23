# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
import json
from shareprice.items import SharepriceItem

BASE_URL = 'http://zk.fm'

class RedditbotSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['https://www.nasdaq.com/']
    start_urls = ['https://www.nasdaq.com/symbol/amzn/historical/']

    def parse(self, response):
        tr = response.css('table tbody tr')
        for p in tr:
            date = map(unicode.strip, p.css('td:nth-child(1)::text').extract())
            opens = map(unicode.strip, p.css('td:nth-child(2)::text').extract())
            high = map(unicode.strip, p.css('td:nth-child(3)::text').extract())
            low = map(unicode.strip, p.css('td:nth-child(4)::text').extract())
            close = map(unicode.strip, p.css('td:nth-child(5)::text').extract())
            volume = map(unicode.strip, p.css('td:nth-child(6)::text').extract())
            for item in zip(date,opens,high,low, close, volume):
                scraped_info = SharepriceItem(date=date, opens=opens, high=high, low=low, close=close, volume=volume)
                yield scraped_info
    
    def start_requests(self): 
        form_data = str("10y|false|AMZN")
        request_body = json.dumps(form_data)
        yield scrapy.Request(self.start_urls[0],
                             method="POST",
                             body=request_body,
                             headers={'Content-Type': 'application/json; charset=UTF-8'}, )