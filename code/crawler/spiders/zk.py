import logging

import scrapy

from crawler.items import MusicItem, ArtistItem
from crawler.spiders.base import BaseSpider


class ZkSpider(BaseSpider):
    name = 'zk'
    allowed_domains = ['zk.fm']
    handle_httpstatus_list = [304, 404]
    base_url = 'https://zk.fm'
    count_page = 10 ** 6

    def start_requests(self):
        if self.test_mode:
            self.count_page = 5

        for n in range(1, self.count_page):
            self.gc_clear()

            yield scrapy.Request(
                url=self.get_url(f'/artist/{n}'),
                errback=self.error,
                callback=self.parse,
            )

    def parse(self, response):
        if response.status in [404]:
            logging.error('Error: 404')
            return

        title_selector = response.css('#container .title_box h1::text').extract_first()
        if not title_selector:
            return

        title = title_selector.rstrip().strip()
        if not title:
            logging.error('Error: encode')
            return

        self.monitor.update_artist_count()
        yield ArtistItem(name=title)

        response.meta['artist_name'] = title
        yield from self.get_items(response)

    def get_items(self, response):
        artist_name = response.meta['artist_name']
        items, items_urls = [], []
        for item in response.css('#container .song'):
            try:
                song_info = {
                    'name': item.css('div.song-name a span::text').extract_first().strip(),
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
            self.monitor.update_song_count()
            yield MusicItem(song_dict)

        next_page = response.css('a.next-btn')
        if next_page and 'disabled' not in next_page.xpath('@class').extract_first():
            url = self.get_url(next_page.xpath('@href').extract_first())
            yield scrapy.Request(
                url,
                meta={
                    'dont_merge_cookie': True,
                    'artist_name': artist_name,
                },
                errback=self.error,
                callback=self.get_items,
            )
