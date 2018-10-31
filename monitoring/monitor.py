from database.connect import db
from storage.queue import redis_queue


class Monitor(object):

    def __init__(self):
        pass

    def run(self):
        pass

    def update_size(self, spider_name, file_type, size, count):
        data = {'spider_name': spider_name, 'file_type': file_type, 'size': size, 'count': count}
        self._emit_size(data)
        db.update(
            'file_size',
            {'file_type': file_type, 'spider_name': spider_name},
            {'$set': data}
        )

    @staticmethod
    def _emit_size(data):
        redis_queue.put({'name': 'file_size', 'data': data})

    def update_memory(self, spider_name, memory):
        data = {'spider_name': spider_name, 'memory': memory}
        self._emit_memory(data)
        db.insert('memory', data)

    @staticmethod
    def _emit_memory(data):
        redis_queue.put({'name': 'memory', 'data': data})
