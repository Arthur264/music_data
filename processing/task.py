from aiohttp import ClientSession

from processing.last_api import LastFmApi


class Task(object):
    last_fm_api = LastFmApi()

    def __init__(self, body, task_type='music', method='GET'):
        self.method = method
        self.task_type = task_type
        self.body = body

    @property
    def is_music_type(self):
        return self.task_type == 'music'

    def __str__(self):
        return f'{self.task_type}_{self.name}'

    async def run(self):
        params = self.last_fm_api.get_song(self.body) if self.is_music_type else self.last_fm_api.get_artist(self.body)
        await self._make_request(headers=params)

    def prepare_result(self):
        pass

    async def _make_request(self, headers):
        async with ClientSession() as session:
            async with session.request(self.method, self.last_fm_api.api_url, headers=headers) as response:
                return await response.text(encoding='utf-8')
