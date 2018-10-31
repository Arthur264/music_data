from time import gmtime, strftime
from database.connect import db
from storage.queue import redis_queue


class Monitor(object):

    def __init__(self):
        self.count = 0

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
        data = {'spider_name': spider_name, 'memory': memory, 'time': strftime("%H:%M:%S", gmtime())}
        self._emit_memory(data)
        db.insert('memory', data)

    def _emit_memory(self, data):
        self.count += 1
        redis_queue.put({'name': 'memory', 'data': data})
