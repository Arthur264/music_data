import asyncio
import io
import logging
import os
import threading
import time
import traceback

import pandas as pd
from tqdm import tqdm

import config
from monitoring.monitor import ProcessMonitor
from processing.task import Task

tqdm.monitor_interval = 0


def get_files(folder_name='results'):
    music_files = []
    artist_files = []
    for path, _, files in os.walk(folder_name):
        for file_name in files:
            file_path = os.path.join(path, file_name)
            _, file_tail = os.path.split(file_path)
            full_path = os.path.abspath(file_path)
            if 'music' in file_tail:
                music_files.append(full_path)
            elif 'artist' in file_tail:
                artist_files.append(full_path)
            else:
                continue

    return music_files, artist_files


def create_folders():
    try:
        os.rmdir(config.PROCESSING_DIR)
        logging.info("Removed folder: 'processing_result'")
    except OSError:
        pass

    try:
        os.makedirs(config.PROCESSING_DIR)
        logging.info("Created folder: 'processing_result'")
    except OSError:
        return


def remove_logs():
    with io.open('log/log.text', 'w'):
        pass


def get_task(files):
    for file_name in files:
        df = pd.read_csv(file_name)
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            row_type = 'song' if row_dict.get('time') else 'artist'
            instance = Task(body=row_dict, task_type=row_type)
            yield instance


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


async def main(loop):
    create_folders()
    remove_logs()
    music_files, artist_files = get_files()
    loop_tasks = [*get_task(music_files), *get_task(artist_files)]

    thread = threading.Thread(target=monitoring_task_count, args=(loop,))
    thread.setDaemon(True)
    thread.start()

    semaphore = asyncio.Semaphore(config.COUNT_TASK_EVENT_LOOP)
    monitor = ProcessMonitor()
    tasks = [asyncio.ensure_future(loop_task.run(semaphore, monitor)) for loop_task in loop_tasks]
    await asyncio.gather(*tasks)


def run():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))
        loop.close()
    except Exception as e:
        with io.open('log/log.txt', 'a') as log_file:
            log_file.write(str(e))
            log_file.write(traceback.format_exc())
