import json
from urllib import urlencode
from urlparse import urlunparse, urlparse
import scrapy

API_KEY = '019606439d302ebbbff19dfeed1c342b'

class MusicApi(object):
    """docstring for Last."""
    api_url = 'http://ws.audioscrobbler.com/2.0/'
    default_params = {
        'api_key': API_KEY,
        'format': 'json'
    }
    def __init__(self):
        pass

    def send_artist(self, name):
        params = {'method': 'artist.getinfo', 'artist': name}
        yield scrapy.Request(self.get_url(params),
                            callback=self._make_artict,
                            meta=params)

    def send_song(self, artist, song):
        params = {'method': 'track.getInfo', 'artist':artist, 'track':song}
        yield scrapy.Request(self.get_url(params),
                            callback=self._make_song,
                            meta=params)



    def get_url(self, params):
        params.update(self.default_params)
        return self.api_url + '?' + urlencode(params)

    def error_request(self, ex, response):
        pass

lastfm = LastFm()
