""" Класс для работы с объектом Group """


from db import SqlQuery


class Group:
    def __init__(self, filter_obj=None):
        self.filter_obj = filter_obj or {}

    def read(self):
        if not self.filter_obj:
            return

        query_params = [self.filter_obj.get('ExternalId')]
        sql_query = SqlQuery(READ_GROUP, query_params)

        return sql_query.execute()

    def upsert(self):
        if not self.filter_obj:
            return

        query_params = [self.filter_obj.get('ExternalId')]
        sql_query = SqlQuery(UPSERT_GROUP, query_params)

        return sql_query.execute()

    def delete(self):
        if not self.filter_obj:
            return

        query_params = [self.filter_obj.get('ExternalId')]
        sql_query = SqlQuery(DELETE_GROUP, query_params)

        return sql_query.execute()


READ_GROUP = """ SELECT * FROM "Group" WHERE """
UPSERT_GROUP = """ INSERT INTO "Group" ("ExternalId") VALUES (?) """
DELETE_GROUP = """ DELETE FROM "Group" WHERE"""
