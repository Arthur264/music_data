from queue import Queue


class PubSub(object):

    def __init__(self):
        self.stack = Queue()

    def add(self, data):
        self.stack.put(data)

    def get(self):
        if not self.stack.empty():
            return self.stack.get()


pub_sub = PubSub()
