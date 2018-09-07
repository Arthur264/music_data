import json
from urllib import urlencode
from music_api import musicApi
from items import MusicItem, ArtistItem
import scrapy

API_KEY = '019606439d302ebbbff19dfeed1c342b'


class LastFm(object):
    """docstring for Last."""
    api_url = 'http://ws.audioscrobbler.com/2.0/'
    default_params = {
        'api_key': API_KEY,
        'format': 'json'
    }
    retry_num = 4

    def __init__(self):
        pass

    @staticmethod
    def get_field(obj, fields):
        if not obj or not fields:
            return None

        result = obj
        for field in fields:
            try:
                result = result[field]
            except (KeyError, IndexError):
                return None
        return result

    def get_artist(self, name):
        params = {'method': 'artist.getinfo', 'artist': name}
        yield scrapy.Request(self.get_url(params),
                             callback=self._make_artist,
                             errback=self.error_request,
                             meta=params)

    def get_song(self, artist, song_info):
        params = {'method': 'track.getInfo', 'artist': artist,
                  'track': song_info['name'], 'item': song_info}
        yield scrapy.Request(self.get_url(params),
                             callback=self._make_song,
                             errback=self.error_request,
                             meta=params)

    def _make_artist(self, response):
        artist_info = {
            'name': response.meta.get('artist'),
        }
        json_response = json.loads(response.body_as_unicode())
        if json_response and not json_response.get('error'):
            artist = json_response['artist']
            artist_info.update({
                'name': self.get_field(artist, ['name']),
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
                    artist_info['similar'].append({'name': similar['name']})
            tags = self.get_field(artist, ['tags', 'tag'])
            if tags:
                for tag in tags:
                    artist_info['tag'].append({'name': tag['name']})

        yield ArtistItem(artist_info)
        for r in musicApi.make_request(artist_info, 'artist'):
            yield r

    def _make_song(self, response):
        song = response.meta.get('item')
        track_info = {
            'name': song['name'],
            'url': song['url'],
            'time': song['time'],
            'artist': song['artist'],
        }
        json_response = json.loads(response.body_as_unicode())
        if json_response and not json_response.get('error'):
            track = json_response['track']
            track_info.update({
                'name': self.get_field(track, ['name']),
                'artist': self.get_field(track, ['artist', 'name']),
                'duration': self.get_field(track, ['duration']),
                'image': self.get_field(track, ['album', 'image', -1, '#text']),
                'listeners_fm': self.get_field(track, ['listeners']),
                'playcount_fm': self.get_field(track, ['playcount']),
            })
        yield MusicItem(track_info)
        for r in musicApi.make_request(track_info, 'song'):
            yield r

    def get_url(self, params):
        params.update(self.default_params)
        return self.api_url + '?' + urlencode(params)

    def error_request(self, exception):
        meta = exception.request.meta
        iteration = meta.get('iteration', 0) + 1
        if iteration < self.retry_num:
            req_url = meta.get("redirect_urls", [exception.request.url])[0]
            request = scrapy.Request(
                url=req_url,
                callback=exception.request.callback,
                errback=exception.request.errback,
                dont_filter=exception.request.dont_filter,
                meta={k: v for k, v in meta.items()}
            )
            request.meta['iteration'] = iteration
            yield request
        else:
            if meta.get('item'):
                yield MusicItem(meta['item'])
                for r in musicApi.make_request(meta.get('item'), 'song'):
                    yield r
            else:
                artist_info = {"name": meta.get('artist')}
                yield ArtistItem(artist_info)
                for r in musicApi.make_request(artist_info, 'artist'):
                    yield r


lastfm = LastFm()
