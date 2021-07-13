import unittest
import db

from group_stat.group_statistics import GroupStatistics
from tests_helpers import sql_base

DEFAULT_EXTERNAL_ID = 'rambler'
DEFAULT_STAT = {
            '@Group': 1,
            'MembersCount': 35
        }


class TestGroupStatistics(unittest.TestCase):
    def setUp(self):
        create_table = db.SqlQuery(sql_base.CREATE_TEST_TABLE)
        create_table.execute()

        stat_dict = DEFAULT_STAT
        self.group_statistics = GroupStatistics(stat_dict)

    def tearDown(self):
        sql_query = db.SqlQuery(sql_base.DROP_TEST_TABLE)
        sql_query.execute()

    def test_update(self, ):
        add_group = db.SqlQuery(""" INSERT INTO "Group" ("ExternalId") VALUES (?)""", [DEFAULT_EXTERNAL_ID])
        add_group.execute()
        self.group_statistics.update()

        group_stat = db.SqlQuery(""" SELECT * FROM "Group" WHERE "ExternalId" = (?) """, [DEFAULT_EXTERNAL_ID])
        result = group_stat.execute()

        self.assertEqual([(1, 'rambler', 35)], result)


if __name__ == "__main__":
    unittest.main()
