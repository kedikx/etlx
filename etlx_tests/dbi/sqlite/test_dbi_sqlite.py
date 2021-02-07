import os
import unittest
from etlx_tests import TestCase
from etlx_tests.dbi import DBI_Test_MixIn
from etlx.dbi.sqlite import DBI_SQLite


class DBI_SQLite_Test(DBI_Test_MixIn, TestCase):

    SQLITE_DB_PATH = "build/etlx_test.db"

    CONNECT = dict(database=SQLITE_DB_PATH)

    @classmethod
    def DBI(cls) -> DBI_SQLite:
        return DBI_SQLite(connect=cls.CONNECT)

    @classmethod
    def setUpClass(cls):
        if os.path.isfile(cls.SQLITE_DB_PATH):
            os.remove(cls.SQLITE_DB_PATH)
        else:
            os.makedirs(os.path.dirname(cls.SQLITE_DB_PATH))
        schema = cls.loadTestData("sqlite/test-schema.sql", local=False)
        stmts = [x for x in schema.split(";\n") if x]
        with cls.DBI() as dbi:
            for sql in stmts:
                try:
                    dbi.execute(sql)
                except Exception as ex:
                    print(ex)


if __name__ == "__main__":
    unittest.main()
