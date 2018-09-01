import sqlite3


class SqliteDataSource:

    def __init__(self, location):
        self.conn = sqlite3.connect(location)

    def close(self):
        self.conn.close()

    def select(self, sql):
        return self.conn.execute(sql)

    def update(self, sql):
        self.conn.execute(sql)
        self.conn.commit()

    def commit(self):
        self.conn.commit()
