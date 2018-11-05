import asyncio
import logging
import os
import traceback
import io

import pandas as pd

from config import PROCESSING_DIR
from processing.task import Task


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
        os.rmdir(PROCESSING_DIR)
        os.makedirs(PROCESSING_DIR)
        logging.info("Created folder: 'processing_result'")
    except OSError:
        return


def get_task(files):
    for file_name in files:
        df = pd.read_csv(file_name)
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            row_type = 'music' if row_dict.get('time') else 'artist'
            instance = Task(body=row_dict, task_type=row_type)
            yield instance


async def main():
    create_folders()
    music_files, artist_files = get_files()
    loop_tasks = [*get_task(music_files), *get_task(artist_files)]

    semaphore = asyncio.Semaphore(100)
    tasks = [asyncio.ensure_future(loop_task.run(semaphore)) for loop_task in loop_tasks]
    await asyncio.gather(*tasks)


def run():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
    except Exception as e:
        with io.open('log/log.txt', 'a') as log_file:
            log_file.write(str(e))
            log_file.write(traceback.format_exc())

