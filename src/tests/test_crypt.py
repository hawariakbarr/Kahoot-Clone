import unittest
from ..utils.crypt import forEncrypt, forDecrypt


class TestCryptMethods(unittest.TestCase):

    def testEncrypt(self):
        self.assertEqual(1,1)
        self.assertEqual(forEncrypt("a"),"b")
        self.assertEqual(forEncrypt("b"),"c")

    def testDecrypt(self):
        self.assertEqual(forDecrypt("b"), "c")
        self.assertEqual(forDecrypt("e"),"d")

if __name__ == "__main__":
    unittest.main()