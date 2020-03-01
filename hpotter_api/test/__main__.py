import unittest
import hpotter_api.test.test_schema

from os.path import dirname, abspath
from os import chdir



# class TestCanTest(unittest.TestCase):

#     def setUp(self):
#         print('setting up...')

#     def test_true_is_true(self):
#         self.assertTrue(1 == 1)

#     def test_false_is_false(self):
#         self.assertFalse(False)

if __name__ == '__main__':

    moduleDir = dirname(abspath(__file__)) + '/'
    chdir(moduleDir)

    from os import getcwd
    print(getcwd())

    from createDb import create_database
    create_database()
    unittest.main()
    