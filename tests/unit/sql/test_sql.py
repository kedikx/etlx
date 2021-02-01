from datetime import datetime  # , date, time
from etlx.sql import SQL

import unittest
from tests import TestCase


class Test_SQL(TestCase):

    def test_0(self):
        sql = SQL()
        self.assertEqual(bool(sql), False)
        self.assertEqual(len(sql), 0)
        self.assertEqual(str(sql), '')

        stmt = 'SELECT * FROM test'
        sql.sql(stmt)
        self.assertEqual(bool(sql), True)
        self.assertEqual(len(sql), len(stmt))
        self.assertEqual(str(sql), stmt)

    def test_1(self):
        sql = SQL().quoted('test')
        self.assertEqual(str(sql), '"test"')
        sql = SQL().quoted('te"st')
        self.assertEqual(str(sql), '"te""st"')

        sql = SQL().arg().arg()
        self.assertEqual(str(sql), '%s%s')
        sql = SQL().kwarg('a').kwarg('b')
        self.assertEqual(str(sql), '%(a)s%(b)s')

        sql = SQL().literal(None)
        self.assertEqual(str(sql), 'NULL')
        sql = SQL().literal(True)
        self.assertEqual(str(sql), '1')
        sql = SQL().literal(False)
        self.assertEqual(str(sql), '0')
        sql = SQL().literal(123)
        self.assertEqual(str(sql), '123')
        sql = SQL().literal(123.456)
        self.assertEqual(str(sql), '123.456')
        dt = datetime(2020, 6, 25, 2, 15, 36)
        sql = SQL().literal(dt)
        self.assertEqual(str(sql), "'2020-06-25 02:15:36'")
        sql = SQL().literal(dt.date())
        self.assertEqual(str(sql), "'2020-06-25'")
        sql = SQL().literal(dt.time())
        self.assertEqual(str(sql), "'02:15:36'")
        sql = SQL().literal("ab'cd%")
        self.assertEqual(str(sql), "'ab''cd%%'")
        sql = SQL().literal(1, 2, 3)
        self.assertEqual(str(sql), "1,2,3")
        sql = SQL().literal(1, (2, 3), 4)
        self.assertEqual(str(sql), "1,(2,3),4")

    def test_SELECT(self):
        sql = SQL().SELECT().FROM('test1')
        self.assertEqual(str(sql), 'SELECT * FROM "test1" ')

        sql = SQL().SELECT('a', 'b').FROM('test2')
        self.assertEqual(str(sql), 'SELECT "a","b" FROM "test2" ')


if __name__ == "__main__":
    unittest.main()
