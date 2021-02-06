import string
import random
from etlx.dbi.abc import DBI

class DBI_Test_MixIn:

    @classmethod
    def DBI(cls) -> DBI: 
        return DBI()

    def randomInt(self, max=2**31):
        return int(random.random()*max)

    def randomString(self, safe=True, n=256):
        s = string.printable
        if safe:
            s = [x for x in s if x not in "'\\%"]
        return ''.join(random.choices(s, k=n))

    def test_dbi_0(self):
        dbi: DBI = self.DBI()
        self.assertEqual(dbi.connected, False)

        dbi.connect()
        self.assertEqual(dbi.connected, True)

        v1 = self.randomInt()
        v2 = self.randomString()
        with dbi.cursor() as cursor:
            cursor.execute(f"SELECT {v1} as c1, '{v2}' as c2")
            row = cursor.fetchone()
            self.assertEqual(cursor.description[0][0], "c1")
            self.assertEqual(row[0], v1)
            self.assertEqual(cursor.description[1][0], "c2")
            self.assertEqual(row[1], v2)

        dbi.commit()
        self.assertEqual(dbi.connected, True)

        dbi.rollback()
        self.assertEqual(dbi.connected, True)

        dbi.close()
        self.assertEqual(dbi.connected, False)

        dbi.close()
        self.assertEqual(dbi.connected, False)

        dbi.rollback()
        self.assertEqual(dbi.connected, False)
        with self.assertRaises(Exception):
            dbi.commit()

    def test_dbi_context_1(self):
        dbi = self.DBI()
        self.assertEqual(dbi.connected, False)
        with dbi:
            self.assertEqual(dbi.connected, True)
        self.assertEqual(dbi.connected, False)

    def test_dbi_context_1_ex(self):
        dbi = self.DBI()
        self.assertEqual(dbi.connected, False)
        with self.assertRaises(RuntimeError):
            try:
                with dbi:
                    self.assertEqual(dbi.connected, True)
                    raise RuntimeError()
            except RuntimeError:
                self.assertEqual(dbi.connected, False)
                raise

    def test_dbi_context_2(self):
        dbi = self.DBI()
        self.assertEqual(dbi.connected, False)

        dbi.connect()
        self.assertEqual(dbi.connected, True)
        with dbi:
            self.assertEqual(dbi.connected, True)
        self.assertEqual(dbi.connected, True)
        dbi.close()
        self.assertEqual(dbi.connected, False)

    def test_dbi_context_2_ex(self):
        dbi = self.DBI()
        self.assertEqual(dbi.connected, False)
        dbi.connect()
        self.assertEqual(dbi.connected, True)
        with self.assertRaises(RuntimeError):
            try:
                with dbi:
                    self.assertEqual(dbi.connected, True)
                    raise RuntimeError()
            except RuntimeError:
                self.assertEqual(dbi.connected, True)
                raise
        self.assertEqual(dbi.connected, True)
        dbi.close()
        self.assertEqual(dbi.connected, False)

    def test_dbi_context_3(self):
        dbi = self.DBI()
        self.assertEqual(dbi.connected, False)
        with dbi:
            self.assertEqual(dbi.connected, True)
            dbi.close()
            self.assertEqual(dbi.connected, False)
        self.assertEqual(dbi.connected, False)

    def test_dbi_1(self):
        with self.DBI() as dbi:
            self.assertEqual(dbi.connected, True)
            dbi.execute("SELECT 123")
        self.assertEqual(dbi.connected, False)

    def test_dbi_2(self):
        v1 = self.randomInt()
        v2 = self.randomString()
        with self.DBI() as dbi:
            self.assertEqual(dbi.connected, True)
            result = dbi.query(f"SELECT {v1} as c1, '{v2}' as c2")
            result = list(result)
            self.assertEqual(len(result), 1)
            row = result[0]
            self.assertEqual(row.c1, v1)
            self.assertEqual(row.c2, v2)
        self.assertEqual(dbi.connected, False)

    def test_dbi_3(self):
        v1 = self.randomInt()
        v2 = self.randomString()
        with self.DBI() as dbi:
            self.assertEqual(dbi.connected, True)
            row = dbi.readone(f"SELECT {v1} as c1, '{v2}' as c2")
            self.assertEqual(row.c1, v1)
            self.assertEqual(row.c2, v2)
        self.assertEqual(dbi.connected, False)

    def test_dbi_sql(self):
        v1 = self.randomString(n=10)
        v2 = self.randomString(n=10)
        v3 = self.randomString(n=10)
        row1 = None

        dbi = self.DBI()
        
        with dbi:
            dbi.sql.INSERT("product", name=v1, description=v2).execute()

        with dbi:
            result = dbi.sql.SELECT().FROM("product").query()
            result = list(result)
            self.assertEqual(len(result), 1)
            row1 = result[0]
            self.assertEqual(row1.name, v1)
            self.assertEqual(row1.description, v2)

        with dbi:
            dbi.sql.UPDATE("product", description=v3).WHERE(id=row1.id).execute()
            dbi.sql.INSERT("product", name=v3, description=v1).execute()

        with dbi:
            result = dbi.sql.SELECT().FROM("product").sql(" ORDER BY id ASC").query()
            result = list(result)
            self.assertEqual(len(result), 2)
            row2 = result[0]
            self.assertEqual(row2.name, v1)
            self.assertEqual(row2.description, v3)

        with dbi:
            dbi.sql.DELETE("product").WHERE(id=row1.id).execute()

        with dbi:
            result = dbi.sql.SELECT().FROM("product").query()
            result = list(result)
            self.assertEqual(len(result), 1)
            row3 = result[0]
            self.assertEqual(row3.name, v3)
            self.assertEqual(row3.description, v1)

