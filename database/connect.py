from pymongo import MongoClient


class Database(object):

    def __init__(self):
        self.conn = MongoClient('localhost', 27017)
        self.cur = self.conn.database

    def connection(self):
        return self.conn

    def remove_table(self, table_name):
        collection = getattr(self.cur, table_name)
        collection.drop()

    def insert(self, table_name, data):
        collection = getattr(self.cur, table_name)
        if isinstance(data, dict):
            collection.insert_one(data)
        else:
            collection.insert_many(data)

    def update(self, table_name, filter, data):
        collection = getattr(self.cur, table_name)
        if isinstance(data, dict):
            collection.update_one(filter, data)
        else:
            collection.update_many(filter, data)

    def find(self, table_name, data=None):
        collection = getattr(self.cur, table_name)
        if data:
            return collection.find(data)

        return collection.find()

    def __del__(self):
        self.cur.close()


db = Database()
