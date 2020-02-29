import unittest
# import schema

class TestCanTest(unittest.TestCase):

    def setUp(self):
        print('setting up...')

    def test_true_is_true(self):
        self.assertTrue(1 == 1)

    def test_false_is_false(self):
        self.assertFalse(False)


if __name__ == '__main__':
    unittest.main()