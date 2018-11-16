import asyncio
import json

from aiohttp import (
    ClientSession,
    ClientError,
)

from processing.last_api import LastFmApi


class Task(object):
    last_fm_api = LastFmApi()
    _default_retries = 4
    _default_timeout = 60

    def __init__(self, body, rotate, task_type='song', method='GET'):
        self.method = method
        self.task_type = task_type
        self.body = body
        self.rotate = rotate

    @property
    def is_song_type(self):
        return self.task_type == 'song'

    @property
    def params(self):
        if self.is_song_type:
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

    async def run(self, semaphore, monitor):
        res = await self._make_request(semaphore)
        res_json = json.loads(res)
        result = self.prepare_result(res_json)
        await self.write_result_in_file(result)
        self.complete(monitor)

    def complete(self, monitor):
        monitor.update_count(self.task_type)

    async def write_result_in_file(self, result):
        await self.rotate.rotate_data(result)

    def prepare_result(self, data):
        if self.is_song_type:
            return self.last_fm_api.make_song(self.body, data)

        return self.last_fm_api.make_artist(self.body, data)

    async def fetch(self, semaphore, session):
        for _ in range(self._default_retries):
            try:
                async with semaphore, session.request(self.method, self.url, timeout=self._default_timeout) as response:
                    return await response.text(encoding='utf-8')
            except (asyncio.TimeoutError, ClientError):
                pass

    async def _make_request(self, semaphore):
        async with ClientSession() as session:
            return await self.fetch(semaphore, session)
