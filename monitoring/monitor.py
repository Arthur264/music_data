from database.connect import db
from pubsub.pubsub import pub_sub


class Monitor(object):

    def __init__(self):
        pass

    def run(self):
        pass

    def update_size(self, spider_name, file_type, size, count):
        data = {'spider_name': spider_name, 'file_type': file_type, 'size': size, 'count': count}
        db.update(
            'file_size',
            {'file_type': file_type, 'spider_name': spider_name},
            {'$set': data}
        )
        self._emit_size(data)

    @staticmethod
    def _emit_size(data):
        pub_sub.add({'name': 'file_size', 'data': data})

    def update_memory(self, spider_name, memory):
        data = {'spider_name': spider_name, 'memory': memory}
        db.insert('memory', data)
        self._emit_memory(data)

    @staticmethod
    def _emit_memory(data):
        pub_sub.add({'name': 'memory', 'data': data})
