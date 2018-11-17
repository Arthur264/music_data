import json

import scrapy

from code.music import MusicItem, ArtistItem
from code.music import BaseSpider

BASE_URL = 'https://solr.jamendo.com/solr/jamcom?rows=1000&q=*&start=25'


class JamEnDoSpider(BaseSpider):
    name = 'jam_en_do'
    song_url = 'https://storage.jamendo.com/download/track/{}/mp35/'
    count_rows = 1000
    api_url = 'https://solr.jamendo.com/solr/jamcom?rows=1000&q=*&start={}'
    start_urls = [api_url.format(0)]

    def parse(self, response):
        start = response.meta.get('start', 0) + self.count_rows
        unique_artist_names = set()
        json_data = json.loads(response.body.decode('utf-8'))['response']['docs']
        self.memory_usage()
        if not json_data:
            return

        for data in json_data:
            artist_name = data['artist_name']
            unique_artist_names.add(artist_name)
            song_info = {
                'name': data['name'],
                'url': self.song_url.format(data['id']),
                'artist': artist_name
            }
            yield MusicItem(song_info)

        for name in unique_artist_names:
            yield ArtistItem(name=name)

        return
        yield scrapy.Request(
            self.api_url.format(start),
            meta={
                'start': start,
            },
            callback=self.parse,
        )
