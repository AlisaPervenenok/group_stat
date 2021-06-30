""" Класс создания запросов к БД SQLite """

import sqlite3

GROUP_STATISTICS_DATABASE = "GroupStatistics.db"


class SqlQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or []

        self.connection = self._create_connection()

    @staticmethod
    def _create_connection():
        connection = None
        try:
            connection = sqlite3.connect(GROUP_STATISTICS_DATABASE)
            return connection
        except sqlite3.DatabaseError as e:
            print("Ошибка соединения с базой: ", e)

        return connection

    def execute(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(self.query, self.params)
            result = cursor.fetchall()
        except sqlite3.DatabaseError as e:
            print("Ошибка выполнения запроса: ", e)
        else:
            self.connection.commit()
            self.connection.close()

            return result
