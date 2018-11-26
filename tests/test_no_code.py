import unittest


class AlwaysPassing(unittest.TestCase):
    def test_sunny(self):
        tests_will_pass = True
        self.assertTrue(tests_will_pass)


if __name__ == '__main__':
    unittest.main()
