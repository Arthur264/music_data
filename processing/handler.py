import asyncio
import os

import pandas as pd
import numpy as np

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


def get_task(files):
    for file_name in files:
        df = pd.read_csv(file_name)
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            row_type = 'music' if row_dict.get('time') else 'artist'
            instance = Task(body=row_dict, task_type=row_type)
            yield instance


def run():
    music_files, artist_files = get_files()
    loop_tasks = [*get_task(music_files), *get_task(artist_files)]
    loop = asyncio.new_event_loop()
    tasks = [loop.create_task(loop_task.run()) for loop_task in loop_tasks]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    loop.close()
