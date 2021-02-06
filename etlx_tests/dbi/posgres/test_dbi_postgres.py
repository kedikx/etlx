import os
import unittest
from etlx_tests import TestCase
from etlx_tests.dbi import DBI_Test_MixIn
from etlx.dbi.postgres import DBI_Postgres


class DBI_Postgres_Test(DBI_Test_MixIn,TestCase):

    CONNECT = dict(
        host=os.getenv("ETLX_TEST_POSTGRES_HOST", "127.0.0.1"),
        port=int(os.getenv("ETLX_TEST_POSTGRES_PORT", "5432")),
        database="etlx_test",
        user="etlx_user",
        password="test",
    )

    @classmethod
    def DBI(cls) -> DBI_Postgres:
        return DBI_Postgres(connect=cls.CONNECT)

    @classmethod
    def setUpClass(cls):
        schema = cls.loadTestData('postgres/test-schema.sql', local=False)
        stmts = [x for x in schema.split(";\n") if x]
        with cls.DBI() as dbi:
            for sql in stmts:
                dbi.execute(sql)

    def test_6(self):
        dbi = self.DBI()
        with dbi:
            rows = dbi.sql.SELECT().sql(" FROM information_schema.TABLES").query()
            rows = list(rows)


if __name__ == "__main__":
    unittest.main()
