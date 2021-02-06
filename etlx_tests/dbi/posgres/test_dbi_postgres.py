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

    def DBI(self) -> DBI_Postgres:
        return DBI_Postgres(connect=self.CONNECT)

    def test_6(self):
        dbi = self.DBI()
        with dbi:
            rows = dbi.sql.SELECT().sql(" FROM information_schema.TABLES").query()
            rows = list(rows)
            print(len(rows))


if __name__ == "__main__":
    unittest.main()
