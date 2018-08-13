# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    artist = scrapy.Field()
    duration = scrapy.Field(default='')
    image = scrapy.Field(default='')
    listeners_fm = scrapy.Field(default='')
    playcount_fm = scrapy.Field(default='')
    tags = scrapy.Field(default=[])


class ArtistItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    image = scrapy.Field(default='')
    listeners_fm = scrapy.Field(default='')
    playcount_fm = scrapy.Field(default='')
    similar = scrapy.Field(default=[])
    tag = scrapy.Field(default=[])
    published = scrapy.Field(default='')
    summary = scrapy.Field(default='')
    content = scrapy.Field(default='')


class TagsItem(scrapy.Item):
    name = scrapy.Field()
