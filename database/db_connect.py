import MySQLdb
class MyDB(object):
    def __init__(self):
        self.connection = MySQLdb.connect("localhost", "root", "", "music")
        self.cur = self.connection.cursor()
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')

    def remove_table(self, name):
        try:
            query = """DROP TABLE {table_name}""".format(table_name=name)
            self.cur.execute(query)
        # print(cursor.fetchall())
        except Exception as e:
            print (e)

    def insert(self, query):
        try:
            self.cur.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            # print("insert error", e)
            self.connection.rollback()
            return False
            

    def query(self, query):
        self.cur.execute(query)
        results = self.cur.fetchall()
        print(results)
        return results

    def __del__(self):
        self.connection.close()
        
        
        
db = MyDB()
