import pickle

import redis


class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.clean()
        self.key = f'{namespace}:{name}'
        self.__db.expire(self.key, 20)

    def qsize(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, item):
        data = pickle.dumps(item)
        self.__db.rpush(self.key, data)

    def get(self, block=True, timeout=None):
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = pickle.loads(item[1])
        return item

    def get_nowait(self):
        return self.get(False)

    def clean(self):
        self.__db.flushdb()


redis_queue = RedisQueue('monitor')
