import json

import scrapy

from crawler.items import MusicItem, ArtistItem
from crawler.spiders.base import BaseSpider


class JamEnDoSpider(BaseSpider):
    name = 'jam_en_do'
    song_url = 'https://storage.jamendo.com/download/track/{}/mp35/'
    count_rows = 1000
    api_url = 'https://solr.jamendo.com/solr/jamcom?rows=1000&q=*&start={0}'
    start_urls = [api_url.format(0)]

    def __init__(self, *args, **kwargs):
        self.custom_settings['DOWNLOAD_DELAY'] = 0.25
        super().__init__(*args, **kwargs)

    def parse(self, response):
        start = response.meta.get('start', 0) + self.count_rows
        unique_artist_names = set()
        json_data = json.loads(response.body.decode('utf-8'))['response']['docs']
        if not json_data:
            return

        for data in json_data:
            artist_name = data['artist_name']
            unique_artist_names.add(artist_name)
            song_info = {
                'name': data['name'],
                'url': self.song_url.format(data['id']),
                'artist': artist_name,
            }
            self.monitor.update_song_count()
            yield MusicItem(song_info)

        for name in unique_artist_names:
            self.monitor.update_artist_count()
            yield ArtistItem(name=name)

        if self.test_mode:
            return

        yield scrapy.Request(
            self.api_url.format(start),
            meta={
                'start': start,
            },
            errback=self.error,
            callback=self.parse,
        )
