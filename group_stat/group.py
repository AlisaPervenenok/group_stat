""" Класс для работы с объектом Group """

import db
from group_stat import constants


class Group:
    def __init__(self, filter_obj=None):
        self.filter_obj = filter_obj or {}

    def insert(self):
        if not self.filter_obj:
            return

        query_params = [self.filter_obj.get('ExternalId')]
        sql_query = db.SqlQuery(INSERT_GROUP, query_params)

        return sql_query.execute()

    @staticmethod
    def read(group_id):
        query_params = [group_id]
        sql_query = db.SqlQuery(READ_GROUP, query_params)

        return sql_query.execute()

    @staticmethod
    def delete(group_id):
        query_params = [group_id]
        sql_query = db.SqlQuery(DELETE_GROUP, query_params)

        return sql_query.execute()


READ_GROUP = """ SELECT * FROM "Group" WHERE "@Group" = (?) """
INSERT_GROUP = """ INSERT INTO "Group" ("ExternalId") VALUES (?) """
DELETE_GROUP = """ DELETE FROM "Group" WHERE "@Group" = (?) """
