from pymongo import MongoClient


class Database(object):

    def __init__(self, name):
        self.db_name = name
        self.conn = MongoClient('localhost', 27017)
        self.cur = getattr(self.conn, self.db_name)

    def connection(self):
        return self.conn

    def cursor(self):
        return self.cur

    def remove_table(self, table_name):
        collection = getattr(self.cur, table_name)
        collection.drop()

    def insert(self, table_name, data):
        collection = getattr(self.cur, table_name)
        if isinstance(data, dict):
            collection.insert_one(data)
        else:
            collection.insert_many(data)

    def update(self, table_name, filter_data, data):
        collection = getattr(self.cur, table_name)
        if isinstance(data, dict):
            collection.update_one(filter_data, data)
        else:
            collection.update_many(filter_data, data)

    def find(self, table_name, data=None):
        collection = getattr(self.cur, table_name)
        if data:
            return collection.find(data)

        return collection.find()

    def delete_db(self):
        self.conn.drop_database(self.db_name)

    def __del__(self):
        self.conn.close()


db = Database('log_database')
