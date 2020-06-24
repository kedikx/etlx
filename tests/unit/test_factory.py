import unittest
from tests import TestCase

from etlx.factory import ServiceFactory

class DummyService:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class TestFunc(TestCase):
    
    def test0(self):
        services = ServiceFactory()

        services.add('DUMMY', DummyService, connect=dict(host='localhost'), other='A')
        self.assertIsNotNone(services.catalog)
        self.assertEqual(len(services.catalog), 1)

        services.add('DUMMY_2', 'DUMMY', connect=dict(host='host2'), other='B')
        self.assertEqual(len(services.catalog), 2)

        services.add('FACTORY', 'etlx.factory.ServiceFactory')
        self.assertEqual(len(services.catalog), 3)

        x = services['DUMMY']
        self.assertEqual(x['other'], 'A')
        self.assertIsNotNone(x)
        x = services.DUMMY()
        self.assertIsNotNone(x)
        self.assertEqual(x.kwargs['other'], 'A')

        x = services['DUMMY_2']
        self.assertEqual(x['other'], 'B')
        self.assertIsNotNone(x)
        x = services.DUMMY_2()
        self.assertIsNotNone(x)
        self.assertEqual(x.kwargs['other'], 'B')
        x = services.DUMMY_2(other='C')
        self.assertIsNotNone(x)
        self.assertEqual(x.kwargs['other'], 'C')

        x = services['FACTORY']
        self.assertIsNotNone(x)

    def test0_1(self):
        services = ServiceFactory()
        with self.assertRaises(ValueError):
            services.add('AAA', 'aaabbbccc')
        with self.assertRaises(AttributeError):
            services.add('BBB', 'etlx.not_exist')

    def test1(self):
        path = self.getTestDataPath('services.yml')

        services = ServiceFactory()
        self.assertIsNotNone(services.catalog)
        self.assertIsNotNone(services.catalog)

        services.load(path)
        self.assertEqual(len(services.catalog), 3)
        
    def test2(self):
        path = self.getTestDataPath('services.yml')

        services = ServiceFactory(path)
        self.assertIsNotNone(services.catalog)
        self.assertEqual(len(services.catalog), 3)

if __name__ == "__main__":
    unittest.main()