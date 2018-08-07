import json
from urllib import urlencode
from music_api import musicApi
from urlparse import urlunparse, urlparse
from music.items import MusicItem, ArtistItem
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

    def get_field(self, obj, fields):
        if not obj or not fields:
            return None

        result = obj
        for field in fields:
            try:
                result = result[field]
            except KeyError, IndexError:
                return None
        return result

    def get_artist(self, name):
        params = {'method': 'artist.getinfo', 'artist': name}
        yield scrapy.Request(self.get_url(params),
                             callback=self._make_artict,
                             errback=self.error_request,
                             meta=params)

    def get_song(self, artist, song_info):
        params = {'method': 'track.getInfo', 'artist': artist,
                  'track': song_info['name'], 'item': song_info}
        yield scrapy.Request(self.get_url(params),
                             callback=self._make_song,
                             errback=self.error_request,
                             meta=params)

    def _make_artict(self, response):
        artict_info = {
            'name': response.meta.get('artist'),
        }
        jsonresponse = json.loads(response.body_as_unicode())
        if jsonresponse and not jsonresponse.get('error'):
            artist = jsonresponse['artist']
            artict_info.update({
                'image': self.get_field(artist, ['image', -2, '#text']),
                'listeners_fm': self.get_field(artist, ['stats', 'listeners']),
                'playcount_fm': self.get_field(artist, ['stats', 'playcount']),
                'similar': [],
                'tag': [],
                'published': self.get_field(artist, ['bio', 'published']).split(',')[0].strip(),
                'content': self.get_field(artist, ['bio', 'content'])
            })
            similars = self.get_field(artist, ['similar', 'artist'])
            if similars:
                for similar in similars:
                    artict_info['similar'].append({'name': similar['name']})
            tags = self.get_field(artist, ['tags', 'tag'])
            if tags:
                for tag in tags:
                    artict_info['tag'].append({'name': tag['name']})

        for r in musicApi.make_request(artict_info, 'artist'):
            yield r

    def _make_song(self, response):
        song = response.meta.get('item')
        track_info = {
            'name': song['name'],
            'url': song['url'],
            'time': song['time'],
            'artist': song['artist'],
        }
        jsonresponse = json.loads(response.body_as_unicode())
        if jsonresponse and not jsonresponse.get('error'):
            track = jsonresponse['track']
            track_info.update({
                'image': self.get_field(track, ['album', 'image', -1, '#text']),
                'listeners_fm': self.get_field(track, ['listeners']),
                'playcount_fm': self.get_field(track, ['playcount']),
            })

        for r in musicApi.make_request(track_info, 'song'):
            yield r

    def get_url(self, params):
        params.update(self.default_params)
        return self.api_url + '?' + urlencode(params)

    def error_request(self, ex, response):
        pass


lastfm = LastFm()
