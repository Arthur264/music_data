import scrapy
import json
import csv
import random
from urlparse import urljoin
from urllib import urlencode
from music.items import MusicItem, ArtistItem

BASE_URL = 'http://zk.fm'
DEFAULT_ARTIST = 'http://www.collectionsocietegenerale.com/data/artiste_a0e33/fiche/4733/large_large_artist_generique_2e4c9.gif'
HEADERS= {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,uk;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'x-client-data': 'CIe2yQEIo7bJAQipncoBCLKdygEI2J3KAQioo8oBGJiYygE='
}


class ZkSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['zk.fm', 'www.google.com']
    
    def start_requests(self): 
        for n in range(0, 10000):
            yield scrapy.Request(url=BASE_URL + '/artist/' + str(n),
                                        meta={'atrict': n, 'proxy': self.get_proxy()}, 
                                        callback=self.parse)

    def parse(self, response):
        title = self.text_encode(response.css("#container .title_box h1::text").extract_first().strip())
        if not title:
            return 
        
        params={'q': title + '+group', 'source': 'lnms', 'tbm': 'isch', 'safe':'active'}
        yield scrapy.Request("https://www.google.com/search?" + urlencode(params),
                    callback =self.getlink,
                    meta={"name": title, 'proxy': self.get_proxy()},
                    headers=HEADERS)

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
            except AttributeError:
                continue
            
            yield MusicItem(artict=atrict, time=song_time, name=song_name, url=song_link)
        
        next_page = response.css("a.next-btn")
        if next_page and 'disabled' not in next_page.xpath("@class").extract_first():
            yield scrapy.Request(self.get_url(next_page.xpath("@href").extract_first()),
                                meta={"atrict": atrict, 'proxy': self.get_proxy()},
                                callback=self.get_items)
            
       
       
    def getlink(self, response):
        title = response.meta['name']
        a = response.css("div.rg_meta::text").extract_first()
        try:
            link =json.loads(a)["ou"]
        except:
            link = DEFAULT_ARTIST
        yield ArtistItem(name=title, image=link)
        
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
    
      