import scrapy


class MusicItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    artist = scrapy.Field()


class ArtistItem(scrapy.Item):
    name = scrapy.Field()


class TagsItem(scrapy.Item):
    name = scrapy.Field()
