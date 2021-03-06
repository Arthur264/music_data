import asyncio
import io
import logging
import os
import threading
import time
import traceback
from itertools import chain, islice

import pandas as pd
from tqdm import tqdm

import config
from monitoring.monitor import ProcessMonitor
from processing.dump_to_file import RotateJsonFile
from processing.task import ProcessingTask
from processing.utils import create_folder, remove_folder, clear_file

tqdm.monitor_interval = 0
COLUMN_NAMES_MUSIC = ('artist', 'name', 'url')
COLUMN_NAMES_ARTIST = ('name',)


def get_files(folder_name='results'):
    music_files = []
    artist_files = []
    for path, _, files in os.walk(folder_name):
        for file_name in files:
            file_path = os.path.join(path, file_name)
            _, file_tail = os.path.split(file_path)
            full_path = os.path.abspath(file_path)
            if 'crawler' in file_tail:
                music_files.append(full_path)
            elif 'artist' in file_tail:
                artist_files.append(full_path)
            else:
                continue

    return music_files, artist_files


def before_processing():
    remove_folder(config.PROCESSING_DIR)
    create_folder(config.PROCESSING_DIR)
    create_folder(config.LOG_FOLDER, exist=True)
    clear_file(config.LOG_FILE)


def get_task(files, rotate, is_artist=False):
    for file_name in files:
        tp = pd.read_csv(
            file_name,
            chunksize=10 * 3,
            low_memory=True,
            names=COLUMN_NAMES_ARTIST if is_artist else COLUMN_NAMES_MUSIC,
        )
        for df in tp:
            for _, row in df.iterrows():
                row_dict = row.to_dict()
                row_type = 'artist' if is_artist else 'song'
                yield ProcessingTask(body=row_dict, task_type=row_type, rotate=rotate)


def monitoring_task_count(loop):
    if not config.DEBUG:
        return

    while True:
        try:
            active_task = len([1 for t in asyncio.Task.all_tasks(loop=loop) if not t.done()])
            logging.info(f'Active tasks count: {active_task}')
            if not active_task:
                break

        except RuntimeError:
            pass

        time.sleep(1)


def make_chunks(iterable, size=10):
    while True:
        result = islice(iterable, size)
        if not result:
            break

        yield result


async def main(loop):
    before_processing()
    music_files, artist_files = get_files()
    rotate_song = RotateJsonFile('song')
    rotate_artist = RotateJsonFile('artist')
    tasks_gen = chain(get_task(music_files, rotate_song), get_task(artist_files, rotate_artist, is_artist=True))

    thread = threading.Thread(target=monitoring_task_count, args=(loop,))
    thread.setDaemon(True)
    thread.start()

    semaphore = asyncio.Semaphore(config.COUNT_TASK_EVENT_LOOP)
    monitor = ProcessMonitor()
    for chucks in make_chunks(tasks_gen, size=config.COUNT_TASK_CHUNKS):
        await asyncio.gather(*[asyncio.ensure_future(chuck.run(semaphore, monitor)) for chuck in chucks])
        await asyncio.gather(*[rotate_artist.complete(), rotate_song.complete()])


def start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main(loop))
    except Exception as e:
        with io.open(config.LOG_FILE, 'a') as log_file:
            log_file.write(str(e))
            log_file.write(traceback.format_exc())
    finally:
        loop.close()
