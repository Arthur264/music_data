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

    @staticmethod
    def get_artist(body):
        return {
            'method': 'artist.getinfo',
            'artist': body['name'],
        }

    @staticmethod
    def get_song(body):
        return {
            'method': 'track.getInfo',
            'artist': body['artist'],
            'track': body['name'],
        }

    def make_artist(self, body, data):
        artist_info = {
            'name': body['name'],
        }
        if data and not data.get('error'):
            artist = data['artist']
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

        return artist_info

    def make_song(self, body, data):
        track_info = {
            'name': body['name'],
            'url': body['url'],
            'time': body['time'],
            'artist': body['artist'],
        }
        if data and not data.get('error'):
            track = data['track']
            track_info.update({
                'name': self.get_field(track, ['name']),
                'artist': self.get_field(track, ['artist', 'name']),
                'duration': self.get_field(track, ['duration']),
                'image': self.get_field(track, ['album', 'image', -1, '#text']),
                'listeners_fm': self.get_field(track, ['listeners']),
                'playcount_fm': self.get_field(track, ['playcount']),
            })
        return track_info

    def get_url(self, params):
        params.update(self.default_params)
        return self.api_url + '?' + urlencode(params)
