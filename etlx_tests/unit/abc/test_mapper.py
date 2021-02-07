from datetime import datetime
from etlx.abc.row import RowDict
from etlx.abc.mapper import RowMapper, ExtractItem, ExtractAttr, ExtractConst, Datetime

import unittest
from etlx_tests import TestCase


class Test_Mapper(TestCase):
    def test_0(self):
        mapper = RowMapper()
        mapper["a"] = ExtractItem("_a")
        mapper["b"] = ExtractAttr("_b")
        mapper["c"] = ExtractConst(3)
        mapper["dt"] = Datetime(ExtractItem("_dt"))
        mapper["dt2"] = Datetime(ExtractItem("_dt2"))

        row = RowDict(_a=1, _b=2, _dt="2020-06-25 03:42:05", _dt2=2020)

        x = mapper(row)
        self.assertEqual(len(x), 5)
        self.assertEqual(x.a, 1)
        self.assertEqual(x.b, 2)
        self.assertEqual(x.c, 3)
        self.assertEqual(x.dt, datetime(2020, 6, 25, 3, 42, 5))
        self.assertEqual(x.dt2, 2020)


if __name__ == "__main__":
    unittest.main()
