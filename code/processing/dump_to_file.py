import json
import os
from abc import abstractmethod

import aiofiles
import numpy as np


class RotateFile(object):
    stack = np.array([])
    max_data_size = 100  # 100 Kb
    file_type = None

    def __init__(self, file_name=None, directory='processing_result'):
        self.directory = directory
        self.filename = file_name
        self.fn = None

    @abstractmethod
    async def write(self):
        pass

    async def rotate_data(self, data):
        self.stack = np.append(self.stack, data)
        stack_size = self.stack.size * self.stack.itemsize / 1024
        if stack_size > self.max_data_size:
            await self.write()

        self.stack = np.array([])

    def __del__(self):
        self.write()

    @property
    def file_name(self):
        return f'{self.filename_template}.{self.file_type}'

    @property
    def filename_template(self):
        return os.path.abspath(os.path.join(self.directory, self.filename))


class RotateJsonFile(RotateFile):
    file_type = 'json'

    async def write(self):
        async with aiofiles.open(self.file_name, mode='a') as infile:
            json_data = '\n'.join(json.dumps(item, ensure_ascii=False) for item in self.stack)
            await infile.write(f'{json_data}\n')
