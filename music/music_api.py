import json
import scrapy

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
Headers = {
    'Accept': 'text/html; q=1.0, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8',
    'User-Agent': USER_AGENT,
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
}


class MusicApi(object):
    api_url = 'http://music-artyr264.c9users.io:8081/api/v1/{}/?format=json'

    def __init__(self):
        pass

    def make_request(self, body, name):
        yield scrapy.Request(self.get_url(name), headers=Headers, method='POST',
                             body=json.dumps(body), meta={'dont_cache': True})

    def get_url(self, url):
        return self.api_url.format(url)


musicApi = MusicApi()
