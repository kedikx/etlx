import unittest
from tests import TestCase

class Test_Dummy(TestCase):

    def test0_getTestDataPath(self):
        sharedDir = self.getTestDir(local=False)
        testDir = self.getTestDir()
        self.assertNotEqual(sharedDir, testDir)

        path = self.getTestDataPath(local=False)
        self.assertEqual(path, sharedDir+'/data')

        path = self.getTestDataPath('dummy.txt', local=False)
        self.assertEqual(path, sharedDir+'/data/dummy.txt')

        path = self.getTestDataPath()
        self.assertEqual(path, testDir+'/data')

        path = self.getTestDataPath('dummy.txt')
        self.assertEqual(path, testDir+'/data/dummy.txt')

    def test1_loadTestData(self):
        data = self.loadTestData('dummy.txt', local=False)
        self.assertEqual(data,'DUMMY')

        data = self.loadTestData('dummy.txt')
        self.assertEqual(data,'DUMMY.LOCAL')


if __name__ == "__main__":
    unittest.main()