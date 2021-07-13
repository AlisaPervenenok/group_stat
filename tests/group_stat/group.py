import unittest
import db

from group_stat.group import Group
from tests_helpers import sql_base


DEFAULT_FILTER_OBJ = {'ExternalId': 'rambler'}
DEFAULT_EXTERNAL_ID = 'rambler'

class TestGroup(unittest.TestCase):
    def setUp(self):
        create_table = db.SqlQuery(sql_base.CREATE_TEST_TABLE)
        create_table.execute()

    def tearDown(self):
        sql_query = db.SqlQuery(sql_base.DROP_TEST_TABLE)
        sql_query.execute()

    def test_insert(self):
        self.group = Group(DEFAULT_FILTER_OBJ)
        self.group.insert()
        group = db.SqlQuery(""" SELECT * FROM "Group" WHERE "ExternalId" = (?) """, [DEFAULT_FILTER_OBJ['ExternalId']])
        result = group.execute()

        self.assertEqual([(1, 'rambler', None)], result)

    def test_read(self):
        add_group = db.SqlQuery(""" INSERT INTO "Group" ("ExternalId") VALUES (?)""", [DEFAULT_EXTERNAL_ID])
        add_group.execute()

        self.group = Group(DEFAULT_FILTER_OBJ)
        result = self.group.read(1)
        self.assertEqual([(1, 'rambler', None)], result)

    def test_delete(self):
        add_group = db.SqlQuery(""" INSERT INTO "Group" ("ExternalId") VALUES (?)""", [DEFAULT_EXTERNAL_ID])
        add_group.execute()

        self.group = Group()
        self.group.delete(1)
        group = db.SqlQuery(""" SELECT * FROM "Group" WHERE @Group" = (?) """, [1])
        result = group.execute()

        self.assertEqual(None, result)


if __name__ == '__main__':
    unittest.main()
