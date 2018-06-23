import scrapy
from urlparse import urljoin
from music.items import MusicItem, ArtistItem

BASE_URL = 'http://zk.fm'

class ZkSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['zk.fm']
    
    def start_requests(self): 
        for n in range(0, 10000):
            yield scrapy.Request(url=BASE_URL + '/artist/' + str(n),meta={'atrict': n}, callback=self.parse)

    def parse(self, response):
        title = self.text_encode(response.css("#container .title_box h1::text").extract_first().strip())
        yield ArtistItem(name=title)

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
            yield scrapy.Request(self.get_url(next_page.xpath("@href").extract_first()),meta={"atrict": atrict}, callback=self.get_items)
            
    @staticmethod
    def text_encode(text):
        try:
            return text.encode('ascii').decode('unicode_escape').encode('utf-8')
        except UnicodeEncodeError:
            return False    
            
    @staticmethod 
    def get_url(url):
        return urljoin(BASE_URL, url) if BASE_URL not in url else url
    
      