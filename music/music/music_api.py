import json
import scrapy
from urlparse import urljoin
import requests

Headers = {
    'Accept': 'text/html; q=1.0, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8',
    'Host': 'music-artyr264.c9users.io:8080',
    'Origin': 'http://music-artyr264.c9users.io:8080',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
}


class MusicApi(object):
    api_url = 'http://music-artyr264.c9users.io:8080/api/v1/{}/?format=json'

    def __init__(self):
        pass

    def make_request(self, body, name):
        yield scrapy.Request(self.get_url(name),headers=Headers, method='POST', body=json.dumps(body))

    def get_url(self, url):
        return self.api_url.format(url)



musicApi = MusicApi()
