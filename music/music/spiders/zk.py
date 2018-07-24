import scrapy
import json
import csv
import random
from urlparse import urljoin
from urllib import urlencode
from music.items import MusicItem, ArtistItem

BASE_URL = 'http://zk.fm'
DEFAULT_ARTIST = 'http://www.collectionsocietegenerale.com/data/artiste_a0e33/fiche/4733/large_large_artist_generique_2e4c9.gif'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,uk;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'x-client-data': 'CIe2yQEIo7bJAQipncoBCLKdygEI2J3KAQioo8oBGJiYygE='
}
HEADERS2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.3'
}


class ZkSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['zk.fm', 'www.google.com']
    handle_httpstatus_list = [304]

    def start_requests(self):
        for n in range(91294, 100000):
            # print("Count:", n)
            yield scrapy.Request(url=BASE_URL + '/artist/' + str(n),
                                 meta={'atrict': n, 'handle_httpstatus_all': True, "dont_merge_cookie": True},
                                 errback=self.error,
                                 headers=HEADERS2,
                                 callback=self.parse)

    def parse(self, response):
        print("url", response.request.url, response.status)
        if response.status in [404]:
            return
        title_selector = response.css("#container .title_box h1::text").extract_first()
        if not title_selector:
            return
        title = title_selector.rstrip().strip()
        if not title:
            return
        # print(response.meta['atrict'], title, DEFAULT_ARTIST)
        yield ArtistItem(id=response.meta['atrict'], name=title, image=DEFAULT_ARTIST)
        # params={'q': title + '+group', 'source': 'lnms', 'tbm': 'isch', 'safe':'active'}
        # yield scrapy.Request("https://www.google.com/search?" + urlencode(params),
        #             callback =self.getlink,
        #             meta={"name": title,'artict': response.meta['atrict'], 'proxy': self.get_proxy()},
        #             headers=HEADERS)

        for r in self.get_items(response):
            yield r

    def get_items(self, response):
        atrict = response.meta['atrict']
        for item in response.css("#container .song"):
            try:
                song_time = item.css("span.song-time::text").extract_first().strip()
                song_name = self.text_encode(item.css("div.song-name a span::text").extract_first().strip())
                if not song_name:
                    continue
                song_link = self.get_url(item.css("span.song-download").xpath('@data-url').extract_first())
            except AttributeError as e:
                continue
            # print(atrict, song_time, song_name, song_link)
            yield MusicItem(artict=atrict, time=song_time, name=song_name, url=song_link)

        next_page = response.css("a.next-btn")
        if next_page and 'disabled' not in next_page.xpath("@class").extract_first():
            yield scrapy.Request(self.get_url(next_page.xpath("@href").extract_first()),
                                 meta={"atrict": atrict, "dont_merge_cookie": True},
                                 headers=HEADERS2,
                                 callback=self.get_items)

    def getlink(self, response):
        a = response.css("div.rg_meta::text").extract_first()
        try:
            link = json.loads(a)["ou"]
        except:
            link = DEFAULT_ARTIST
        yield ArtistItem(id=response.meta['artict'], name=response.meta['name'], image=link)

    @staticmethod
    def text_encode(text):
        try:
            return text.encode('ascii').decode('unicode_escape').encode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            return False

    @staticmethod
    def get_url(url):
        return urljoin(BASE_URL, url) if BASE_URL not in url else url

    def get_proxy(self):
        proxy = random.choice(self.get_proxy_factory())
        return "https://ebates:w2zQbyMp@%s:60099" % proxy

    @staticmethod
    def get_proxy_factory():
        result = []
        with open("music/proxylist.csv") as f:
            reader = csv.reader(f)
            for idx, item in enumerate(reader):
                result.append(item[0])
        return result

    def error(e, response):
        # import pdb; pdb.set_trace()
        print("Error:", e, response)
        return True
