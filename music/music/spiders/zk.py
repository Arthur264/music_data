import scrapy
import csv
import random
from urlparse import urljoin
from last_api import lastfm

BASE_URL = 'http://zk.fm'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.3'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8',
    'User-Agent': USER_AGENT
}


class ZkSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['zk.fm', 'ws.audioscrobbler.com', 'music-artyr264.c9users.io']
    handle_httpstatus_list = [304, 404]

    def __init__(self, start=None, *a, **kw):
        super(ZkSpider, self).__init__(*a, **kw)
        self.start = start

    def start_requests(self):
        for n in range(self.start, self.start + 20):
            yield scrapy.Request(url=BASE_URL + '/artist/' + str(n),
                                 meta={'artist': n, 'handle_httpstatus_all': True, "dont_merge_cookie": True},
                                 errback=self.error,
                                 headers=HEADERS,
                                 callback=self.parse)

    def parse(self, response):
        if response.status in [404]:
            print('Error: 404')
            return
        title_selector = response.css("#container .title_box h1::text").extract_first()
        if not title_selector:
            return
        title = self.text_encode(title_selector.rstrip().strip())
        if not title:
            print('Error: encode')
            return
        for r in lastfm.get_artist(title):
            yield r

        response.meta['artist_name'] = title
        for r in self.get_items(response):
            yield r

    def get_items(self, response):
        artist = response.meta['artist']
        artist_name = response.meta['artist_name']
        for item in response.css("#container .song"):
            try:
                song_info = {
                    'name': self.text_encode(item.css("div.song-name a span::text").extract_first().strip()),
                    'time': item.css("span.song-time::text").extract_first().strip(),
                    'url': self.get_url(item.css("span.song-download").xpath('@data-url').extract_first()),
                    'artist': artist_name
                }
                if not song_info['name']:
                    continue
            except AttributeError as e:
                continue

            for r in lastfm.get_song(artist_name, song_info):
                yield r
        next_page = response.css("a.next-btn")
        if next_page and 'disabled' not in next_page.xpath("@class").extract_first():
            url = self.get_url(next_page.xpath("@href").extract_first())
            yield scrapy.Request(url,
                                 meta={
                                     "artist": artist, "dont_merge_cookie": True, 'artist_name': artist_name},
                                 headers=HEADERS,
                                 callback=self.get_items)

    @staticmethod
    def text_encode(text):
        try:
            return unicode(text.encode('utf-8'))
        except (UnicodeEncodeError, UnicodeDecodeError):
            return None

    @staticmethod
    def get_url(url):
        return urljoin(BASE_URL, url)

    def get_proxy(self):
        proxy = random.choice(self.get_proxy_factory())
        return "" % proxy

    @staticmethod
    def get_proxy_factory():
        result = []
        with open("music/proxylist.csv") as f:
            reader = csv.reader(f)
            for idx, item in enumerate(reader):
                result.append(item[0])
        return result

    @staticmethod
    def error(response):
        print("Error:", response)
        return True
