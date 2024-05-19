import unittest
import hashlib

from src.hashing.hash import HashingFactory


class HashTest(unittest.TestCase):

    def setUp(self):
        self.factory = HashingFactory()

    def test_padding(self):
        # padding for 'Hello' message
        self.assertEqual(self.factory._pad(
                         self.factory._convert('Hello')).hex(),
                         '48656c6c6f8000000000000000000000'
                         '00000000000000000000000000000000'
                         '00000000000000000000000000000000'
                         '00000000000000000000000000000028')

    def test_schedule(self):
        block = self.factory._pad(self.factory._convert('Hello'))
        schedule = self.factory._schedule(block)
        self.assertEqual(list(map(lambda el: el.hex(), schedule)),
                         ['48656c6c', '6f800000', '00000000', '00000000',
                          '00000000', '00000000', '00000000', '00000000',
                          '00000000', '00000000', '00000000', '00000000',
                          '00000000', '00000000', '00000000', '00000028',
                          '5594884c', '6f910000', 'd53ac55a', 'a01bde7a',
                          '3a337e8b', '94da02f9', 'd09a76a8', '969b56c2',
                          'e54654c3', '96d784a5', '80dcbe18', '6d174adb',
                          '5dc96a53', '1cc815a3', '7f1a0dce', '9db3e25f',
                          '80da5dc2', '9c0ca81e', 'bea91b8b', '8da1af1a',
                          '66a32861', 'cc59ddf4', 'a1c28a29', 'fb405db4',
                          '4eaacb84', '896ee197', 'b4ed8def', '782c4a4a',
                          'e252b57c', '7b6c0231', 'da9ee233', '700956f3',
                          'bc709c4d', '1900a949', 'e3bfb13b', 'b581cf14',
                          '980047e9', '6b30284b', '9eef960a', '7c902e42',
                          '27e9ffc6', '2ab47040', 'b3e8da4f', '0f211a94',
                          '30dcba1f', '8ce0fd92', 'decd3e41', 'a5312439'])

    def test_empty_message(self):
        message = ''
        self.assertEqual(self.factory.hash(message).hex(), hashlib.sha256(
            message.encode('ascii')).hexdigest())

    def test_some_text(self):
        message = 'some text'
        self.assertEqual(self.factory.hash(message).hex(), hashlib.sha256(
            message.encode('ascii')).hexdigest())

    def test_lol_kek(self):
        message = 'lol kek'
        self.assertEqual(self.factory.hash(message).hex(), hashlib.sha256(
            message.encode('ascii')).hexdigest())


if __name__ == '__main__':
    unittest.main(verbosity=2)
