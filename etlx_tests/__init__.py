import unittest
import os
import inspect


class TestCase(unittest.TestCase):
    """Base class for unittest style tests"""

    DATA_DIR_NAME = "data"

    @classmethod
    def getTestDir(cls, local=True) -> str:
        """Returns directory of the source file"""
        return os.path.dirname(inspect.getfile(cls) if local else __file__)

    @classmethod
    def getTestDataPath(cls, relativePath=None, local=True) -> str:
        """Returns full path to data bound to TestCase.
        The path is based on location of the source file:
        path = dir(file(class))/data/<relativePath>
        """
        testDir = cls.getTestDir(local)
        testDataDir = os.path.join(testDir, cls.DATA_DIR_NAME)
        if not relativePath:
            return testDataDir
        return os.path.join(testDataDir, relativePath)

    @classmethod
    def loadTestData(cls, relativePath, local=True):
        path = cls.getTestDataPath(relativePath, local)
        with open(path, "r") as f:
            return f.read()
