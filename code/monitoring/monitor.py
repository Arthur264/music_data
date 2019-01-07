from time import gmtime, strftime

from storage.queue import redis_queue
from config import COUNT_EMIT_FILE_SIZE


class BaseMonitor(object):

    def __init__(self):
        pass

    def __str__(self):
        return 'BaseMonitor'

    @staticmethod
    def _emit_event(name, data):
        redis_queue.put({'name': name, 'data': data})


class CrawlerMonitor(BaseMonitor):

    def __str__(self):
        return 'CrawlerMonitor'

    def update_size(self, spider_name, file_type, size, count):
        data = {'spider_name': spider_name, 'file_type': file_type, 'size': size, 'count': count}
        self._emit_event('file_size', data)
        db.update(
            'file_size',
            {'file_type': file_type, 'spider_name': spider_name},
            {'$set': data}
        )

    def update_memory(self, spider_name, memory):
        data = {'spider_name': spider_name, 'memory': memory, 'time': strftime("%H:%M:%S", gmtime())}
        self._emit_event('memory', data)
        db.insert('memory', data)


class ProcessMonitor(BaseMonitor):
    storage = {}

    def __init__(self):
        super().__init__()
        db.insert('process_item', [
            {'file_type': 'song', 'count': 0},
            {'file_type': 'artist', 'count': 0}
        ])

    def __str__(self):
        return 'ProcessMonitor'

    def update_count(self, task_type):
        count_tasks = self.storage.get(task_type, 0)
        self.storage[task_type] = count_tasks + 1

        if count_tasks and count_tasks % COUNT_EMIT_FILE_SIZE == 0:
            data = {'file_type': task_type, 'count': count_tasks}
            self._emit_event('process_item', data)
            db.update(
                'process_item',
                {'file_type': task_type},
                {'$set': {'count': count_tasks}}
            )
