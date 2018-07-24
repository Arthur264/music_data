from urllib.parse import urljoine, urlencode, urlunparse, urlparse
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
                            meta=params,
                            errorback=self.error_request)

    def get_song(self, artist, song):
        params = {'method': 'track.getInfo', 'artist':artist, 'track':song}
        yield scrapy.Request(self.get_url(params),
                            callback=self._make_song,
                            meta=params,
                            errorback=self.error_request)

    def _make_artict(self, response):
        params = response.meta.get('params')
        jsonresponse = json.loads(response.body_as_unicode())



    def get_url(params = {}):
        parser = urlparse(self.api_url)
        params.update(default_params)
        parser[4] = urlencode(query_params)
        return urlparse.urlunparse(parser)

lastfm = LastFm()
