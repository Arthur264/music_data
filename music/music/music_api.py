import json
import scrapy

Headers = {
    'Accept': 'text/html; q=1.0, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8',
    'Host': 'music-artyr264.c9users.io:8081',
    'Origin': 'http://music-artyr264.c9users.io:8081',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
}


class MusicApi(object):
    api_url = 'http://music-artyr264.c9users.io:8081/api/v1/{}/?format=json'

    def __init__(self):
        pass

    def make_request(self, body, name):
        yield scrapy.Request(self.get_url(name), headers=Headers, method='POST', body=json.dumps(body))

    def get_url(self, url):
        return self.api_url.format(url)


musicApi = MusicApi()
