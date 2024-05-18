import unittest
import hashlib
from src.hashing.hash import HashingFactory


class HashTest(unittest.TestCase):

    def SetUp(self):
        self.factory = HashingFactory()

    def test_empty_message(self):
        message = ''
        self.assertEqual(self.factory.hash(message), hashlib.sha256(message))

    def test_some_text(self):
        message = 'some text'
        self.assertEqual(self.factory.hash(message), hashlib.sha256(message))

    def test_lol_kek(self):
        message = 'lol kek'
        self.assertEqual(self.factory.hash(message), hashlib.sha256(message))


if __name__ == '__main__':
    unittest.main()
