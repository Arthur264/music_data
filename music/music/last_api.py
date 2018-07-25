import json
from urllib import urlencode
from urlparse import urlunparse, urlparse
import scrapy

API_KEY = '019606439d302ebbbff19dfeed1c342b'

class LastFm(object):
    """docstring for Last."""
    api_url = 'http://ws.audioscrobbler.com/2.0/'
    default_params = {
        'api_key': API_KEY,
        'format': 'json'
    }
    def __init__(self):
        pass

    def get_artist(self, name):
        params = {'method': 'artist.getinfo', 'artist': name}
        yield scrapy.Request(self.get_url(params),
                            callback=self._make_artict,
                            meta=params)

    def get_song(self, artist, song):
        params = {'method': 'track.getInfo', 'artist':artist, 'track':song}
        yield scrapy.Request(self.get_url(params),
                            callback=self._make_song,
                            meta=params)

    def _make_artict(self, response):
        params = response.meta.get('params')
        jsonresponse = json.loads(response.body_as_unicode())
        artist = jsonresponse['artist']
            artict_info = {
            'name': artist['name'],
            'image': artist['image'][-2]['#text'],
            'listeners': artist['stats']['listeners'],
            'playcount': artist['stats']['playcount'],
            'similar': [],
            'tags': [],
            'biography': {
                'published': artist['bio']['published'],
                'summary': artist['bio']['summary'],
                'content': artist['bio']['content']
            }
        }
        for similar in artist['similar']['artist']:
            artict_info['similar'].append({'name': similar['name']})
        for tag in artist['tags']['tag']:
            artict_info['tags'].append({'name': tag['name']})

    def _make_song(self, response):
        params = response.meta.get('params')
        jsonresponse = json.loads(response.body_as_unicode())
        # print(jsonresponse)


    def get_url(self, params):
        params.update(self.default_params)
        return self.api_url + '?' + urlencode(params)

    def error_request(self, ex, response):
        pass

lastfm = LastFm()
