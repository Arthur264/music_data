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
    handle_httpstatus_list = [304, 404]
    start_urls = ['https://solr.jamendo.com/solr/jamcom?rows=1000&q=*&start=25']

    def parse(self, response):
        unique_artist_names = set()
        json_data = json.loads(response.body.decode('utf-8'))['response']['docs']
        for data in json_data:
            unique_artist_names.add(data['album_name'])
            song_info = {
                'name': data['name'],
                'url': self.get_url(item.css('span.song-download').xpath('@data-url').extract_first()),
                'artist': artist_name
            }

        for artist_name in unique_artist_names:
            yield ArtistItem(name=artist_name)

    def get_items(self, response):
        artist_name = response.meta['artist_name']
        items, items_urls = [], []
        for item in response.css('#container .song'):
            try:
                song_info = {
                    'name': item.css('div.song-name a span::text').extract_first().strip(),
                    'time': item.css('span.song-time::text').extract_first().strip(),
                    'url': self.get_url(item.css('span.song-download').xpath('@data-url').extract_first()),
                    'artist': artist_name
                }
                if not song_info['name']:
                    continue

                if song_info['url'] not in items_urls:
                    items_urls.append(song_info['url'])
                    items.append(song_info)

            except AttributeError:
                continue

        for song_dict in items:
            yield MusicItem(song_dict)

        self.memory_usage()

        next_page = response.css('a.next-btn')
        if next_page and 'disabled' not in next_page.xpath('@class').extract_first():
            url = self.get_url(next_page.xpath('@href').extract_first())
            yield scrapy.Request(
                url,
                meta={
                    'dont_merge_cookie': True,
                    'artist_name': artist_name,
                },
                headers=HEADERS,
                callback=self.get_items,
            )
