import os

import pandas as pd

from processing.task import Task


def get_files(folder_name='results'):
    music_files = []
    artist_files = []
    for path, _, files in os.walk(folder_name):
        for file_name in files:
            file_path = os.path.join(path, file_name)
            if 'music' in file_path:
                music_files.append(file_path)
            elif 'artist' in file_path:
                artist_files.append(file_path)
            else:
                continue
    return music_files, artist_files


def get_task(files):
    tasks = []
    for file_name in files:
        df = pd.read_json(file_name)
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            if row_dict.get('time'):
                instance = Task()
            else:
                instance = Task()
            tasks.append(instance)


def run():
    music_files, artist_files = get_files()
    tasks = [get_task(music_files), get_task(artist_files)]
