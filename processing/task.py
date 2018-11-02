import json

import aiofiles
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

    @property
    def params(self):
        if self.is_music_type:
            return self.last_fm_api.get_song(self.body)

        return self.last_fm_api.get_artist(self.body)

    @property
    def name(self):
        return self.body['name']

    @property
    def url(self):
        return self.last_fm_api.get_url(self.params)

    def __str__(self):
        return f'{self.task_type}_{self.name}'

    async def run(self, semaphore):
        res = await self._make_request(semaphore)
        res_json = json.loads(res)
        result = self.prepare_result(res_json)
        return await self.write_result_in_file(result)

    async def write_result_in_file(self, result):
        async with aiofiles.open(f'processing_result/{self.task_type}.csv', 'a') as out_file:
            data = ','.join(list(result.values()))
            await out_file.write(data)
            await out_file.flush()

    def prepare_result(self, data):
        if self.is_music_type:
            return self.last_fm_api.make_song(self.body, data)

        return self.last_fm_api.make_artist(self.body, data)

    async def fetch(self, semaphore, session):
        async with semaphore, session.request(self.method, self.url) as response:
            return await response.text(encoding='utf-8')

    async def _make_request(self, semaphore):
        async with ClientSession() as session:
            return await self.fetch(semaphore, session)
