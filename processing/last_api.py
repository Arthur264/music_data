import json
from urllib.parse import urlencode


class LastFmApi(object):
    api_url = 'http://ws.audioscrobbler.com/2.0/'
    api_key = '019606439d302ebbbff19dfeed1c342b'
    default_params = {
        'api_key': api_key,
        'format': 'json'
    }

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

    def get_artist(self, body):
        return {
            'method': 'artist.getinfo',
            'artist': body['name'],
        }

    def get_song(self, body):
        return {
            'method': 'track.getInfo',
            'artist': body['artist'],
            'track': body['name'],
        }

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

    def get_url(self, params):
        params.update(self.default_params)
        return self.api_url + '?' + urlencode(params)



