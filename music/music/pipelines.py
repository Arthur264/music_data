from scrapy import log
from music_api import musicApi
from scrapy.contrib.pipeline.media import MediaPipeline


class MusicPipeline(MediaPipeline):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        api_name = 'song' if item.__class__.__name__ == "MusicItem" else 'artist'
        for r in musicApi.make_request(dict(item), api_name):
            yield r
        return
