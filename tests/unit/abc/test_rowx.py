from etlx.abc import RowX

import unittest
#from tests import TestCase

class Test_abc_RowX(unittest.TestCase):

    def test01_interface_obj(self):
        x = RowX()
        x.A = 'A'
        v = x.A
        self.assertEqual(v,'A')

    def test02_interface_dict(self):
        x = RowX()
        x['B'] = 'B'
        v = x['B']
        self.assertEqual(v,'B')

    def test11_update_kwargs(self):
        x = RowX()
        x.update(A='A', B='B')
        self.assertEqual(x.A,'A')
        self.assertEqual(x.B,'B')

    def test12_update_seq(self):
        x = RowX()
        x.update([('A','A'), ('B','B')])
        self.assertEqual(x.A,'A')
        self.assertEqual(x.B,'B')

    def test13_update_dict(self):
        x = RowX()
        x.update({'A':'A', 'B':'B'})
        self.assertEqual(x.A,'A')
        self.assertEqual(x.B,'B')

if __name__ == "__main__":
    unittest.main()    