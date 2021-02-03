from datetime import datetime  # , date, time
from etlx.sql import SQL

import unittest
from etlx_tests import TestCase


class Test_SQL(TestCase):
    def test_0(self):
        sql = SQL()
        self.assertEqual(bool(sql), False)
        self.assertEqual(len(sql), 0)
        self.assertEqual(str(sql), "")

        stmt = "SELECT * FROM test"
        sql.sql(stmt)
        self.assertEqual(bool(sql), True)
        self.assertEqual(len(sql), len(stmt))
        self.assertEqual(str(sql), stmt)

    def test_1(self):
        sql = SQL().quoted("test")
        self.assertEqual(str(sql), '"test"')
        sql = SQL().quoted('te"st')
        self.assertEqual(str(sql), '"te""st"')

        sql = SQL().arg().arg()
        self.assertEqual(str(sql), "%s%s")
        sql = SQL().kwarg("a").kwarg("b")
        self.assertEqual(str(sql), "%(a)s%(b)s")

        sql = SQL().literal(None)
        self.assertEqual(str(sql), "NULL")
        sql = SQL().literal(True)
        self.assertEqual(str(sql), "1")
        sql = SQL().literal(False)
        self.assertEqual(str(sql), "0")
        sql = SQL().literal(123)
        self.assertEqual(str(sql), "123")
        sql = SQL().literal(123.456)
        self.assertEqual(str(sql), "123.456")
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
        sql = SQL().SELECT().FROM("test1")
        self.assertEqual(str(sql), 'SELECT * FROM "test1"')

        sql = SQL().SELECT("a", "b").FROM("test2")
        self.assertEqual(str(sql), 'SELECT "a","b" FROM "test2"')

        sql = SQL().SELECT("a", "b").FROM("test2").WHERE(**{"a b c": 3})
        self.assertEqual(str(sql), 'SELECT "a","b" FROM "test2" WHERE "a b c"=3')

    def test_INSERT(self):
        sql = SQL().INSERT("test", a=1, b=2)
        self.assertEqual(str(sql), 'INSERT INTO "test" ("a","b") VALUES (1,2)')

    def test_INSERT_CV(self):
        sql = SQL().INSERT_CV("test", ("a", "b"), (1, 2))
        self.assertEqual(str(sql), 'INSERT INTO "test" ("a","b") VALUES (1,2)')

    def test_UPDATE(self):
        sql = SQL().UPDATE("test", a=1, b=2)
        self.assertEqual(str(sql), 'UPDATE "test" SET "a"=1,"b"=2')

    def test_UPDATE_CV(self):
        sql = SQL().UPDATE_CV("test", ("a", "b"), (1, 2))
        self.assertEqual(str(sql), 'UPDATE "test" SET "a"=1,"b"=2')

    def test_DELETE(self):
        sql = SQL().DELETE("test")
        self.assertEqual(str(sql), 'DELETE FROM "test"')


if __name__ == "__main__":
    unittest.main()
