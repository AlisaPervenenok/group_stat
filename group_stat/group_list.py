""" Класс списочного метода GroupList """

from group_stat import constants
import db


class GroupList:

    def __init__(self, filter_obj=None):
        self.filter_obj = filter_obj or {}
        self._prepare_filter()
        self.query = self._prepare_query()

    def _prepare_filter(self):
        if not isinstance(self.filter_obj, dict):
            raise Warning(
                "Передан некорректный тип параметра - фильтр списочного метода get_group_list должен иметь тип dict!"
            )
        for key, value in self.filter_obj.items():
            if key not in constants.GROUP_FILTER_DICT:
                self.filter_obj.pop(key)
            expected_field_type = constants.GROUP_FILTER_DICT[key]
            if not isinstance(value, expected_field_type):
                raise Warning(
                    f"Передан некорректный тип поля {key}, ожидается {expected_field_type}")
        return self.filter_obj

    def _prepare_query(self):

        if not self.filter_obj:
            return GET_GROUP_LIST_BASE

        where_base = """ WHERE "@Group" IS NOT NULL """

        for key, value in self.filter_obj .items():
            where_base += f""", {key} = ANY({value})"""

        return GET_GROUP_LIST_BASE + where_base

    def get(self):
        sql_query = db.SqlQuery(self.query)
        return sql_query.execute()


GET_GROUP_LIST_BASE = """ SELECT "@Group", "ExternalId" FROM "Group" """
