import io
import logging
import os
from itertools import islice


def create_folder(directory, exist=False):
    try:
        os.makedirs(directory, exist_ok=exist)
        logging.info(f'Created folder: {directory}')
    except OSError:
        return


def remove_folder(directory):
    try:
        os.rmdir(directory)
        logging.info(f'Removed folder: {directory}')
    except OSError:
        pass


def clear_file(path):
    with io.open(path, 'w'):
        pass


def make_chunks(iterable, size=10):
    while size:
        size -= 1
        result = islice(iterable, size)
        if not result:
            break

        yield result
