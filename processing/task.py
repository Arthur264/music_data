from aiohttp import ClientSession

from processing.last_api import LastFmApi


class Task(object):
    last_fm_api = LastFmApi()

    def __init__(self, name, spider_name, body, task_type='music', method='GET'):
        self.name = name
        self.spider_name = spider_name
        self.method = method
        self.task_type = task_type
        self.body = body

    async def run(self):
        pass

    def prepare_result(self):
        pass

    async def make_request(self):
        async with ClientSession() as session:
            async with session.request(self.method) as response:
                return await response.text(encoding='utf-8')
