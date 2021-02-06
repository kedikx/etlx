import os
import unittest
from etlx_tests import TestCase
from etlx_tests.dbi import DBI_Test_MixIn
from etlx.dbi.mysql import DBI_MySQL


class DBI_MySQLdb_Test(DBI_Test_MixIn,TestCase):

    CONNECT = dict(
        host=os.getenv("ETLX_TEST_MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("ETLX_TEST_MYSQL_PORT", "3306")),
        database="etlx_test",
        user="etlx_user",
        password="test",
    )

    @classmethod
    def DBI(cls) -> DBI_MySQL:
        return DBI_MySQL(connect=cls.CONNECT)

    @classmethod
    def setUpClass(cls):
        schema = cls.loadTestData('mysql/test-schema.sql', local=False)
        stmts = [x for x in schema.split(";\n") if x]
        with cls.DBI() as dbi:
            for sql in stmts:
                dbi.execute(sql)

    def test_mysql_schema(self):
        dbi = self.DBI()
        with dbi:
            rows = dbi.sql.SELECT().FROM("TABLES", "information_schema").query()
            rows = list(rows)
            print(len(rows))


if __name__ == "__main__":
    unittest.main()
