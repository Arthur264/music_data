import io
import json
import os
from abc import abstractmethod

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
    def write(self):
        pass

    def rotate_data(self, data):
        self.stack = np.append(self.stack, data)
        stack_size = self.stack.size * self.stack.itemsize / 1024
        if stack_size > self.max_data_size:
            self.write()

    def __del__(self):
        self.write()

    @property
    def filename_template(self):
        return os.path.abspath(os.path.join(self.directory, self.filename))


class RotateJsonFile(RotateFile):
    file_type = 'json'

    def write(self):
        with io.open(f'{self.filename_template}.{self.file_type}', 'a') as out_file:
            json.dump(self.stack.tolist(), out_file, ensure_ascii=False)

        self.stack = np.array([])
