import json

import scrapy

from music.items import MusicItem, ArtistItem
from music.spiders.base import BaseSpider

BASE_URL = 'https://solr.jamendo.com/solr/jamcom?rows=1000&q=*&start=25'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8',
    'User-Agent': USER_AGENT
}


class JamEnDoSpider(BaseSpider):
    name = 'jam_en_do'
    song_url = 'https://storage.jamendo.com/download/track/{}/mp35/'
    api_url = 'https://solr.jamendo.com/solr/jamcom?rows=1000&q=*&start={}'
    start_urls = [api_url.format(0)]

    def parse(self, response):
        start = response.meta.get('start', 0) + 1000
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

        yield scrapy.Request(
            self.api_url.format(start),
            meta={
                'start': start,
            },
            headers=HEADERS,
            callback=self.parse,
        )

