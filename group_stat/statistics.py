""" Класс работы со статистикой групп """
from db import SqlQuery


class GroupStatistics:
    def __init__(self, stat_dict=None):
        self.stat_dict = stat_dict or {}
        self.group = self.stat_dict.get('@Group')
        self.members_count = self.stat_dict.get('MembersCount')

    def update(self):
        params = [self.members_count, self.group]
        sql_query = SqlQuery(UPDATE_GROUP_STATISTICS, params)

        return sql_query.execute()

    @staticmethod
    def get():
        sql_query = SqlQuery(GET_GROUP_STATISTICS)
        return sql_query.execute()


UPDATE_GROUP_STATISTICS = """ UPDATE "Group" SET "MembersCount"=? WHERE "@Group"=? """
GET_GROUP_STATISTICS = """ SELECT * FROM "Group" """
