import os
import unittest
from etlx_tests import TestCase
from etlx.dbi.mysql import DBI_MySQL


class DBI_MySQLdb_Test(TestCase):

    CONNECT = dict(
        host = os.getenv("ETLX_TEST_MYSQL_HOST", "127.0.0.1"),
        port = int(os.getenv("ETLX_TEST_MYSQL_PORT", "3306")),
        database="etlx_test",
        user="etlx_user",
        password="test",
    )

    def getTestDBI(self):
        return DBI_MySQL(connect=self.CONNECT)

    def test_0(self):
        with self.getTestDBI() as dbi:
            self.assertEqual(dbi.database, "etlx_test")
            cursor = dbi.execute("SELECT 'test_0' as value")
            self.assertIsNotNone(cursor)

        dbi.rollback()
        dbi.close()

    def test_1(self):
        dbi = self.getTestDBI()
        dbi.connect()
        self.assertEqual(dbi.database, "etlx_test")
        with dbi:
            row = dbi.readone("SELECT 'test_1' as value")
            self.assertIsNotNone(row.value)
            self.assertEqual(row.value, "test_1")
        dbi.close()

    def test_2(self):
        dbi = self.getTestDBI()
        with dbi:
            row = dbi.readone("SELECT 'test_1' as value")
            self.assertIsNotNone(row.value)
            self.assertEqual(row.value, "test_1")
            dbi.rollback()
            dbi.close()

    def test_4(self):
        dbi = self.getTestDBI()
        with dbi:
            self.assertEqual(dbi.database, "etlx_test")
            rows = list(dbi.query("SELECT 'test_1' as value"))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].value, "test_1")
            dbi.rollback()
            dbi.close()

    def test_5(self):
        dbi = self.getTestDBI()
        try:
            with dbi:
                raise RuntimeError()
        except RuntimeError:
            pass

    def test_6(self):
        dbi = self.getTestDBI()
        with dbi:
            rows = dbi.sql.SELECT().FROM("TABLES", "information_schema").query()
            rows = list(rows)
            print(len(rows))


if __name__ == "__main__":
    unittest.main()
