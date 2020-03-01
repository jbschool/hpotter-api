import unittest

from os.path import dirname, abspath
from os import chdir

moduleDir = dirname(abspath(__file__)) + '/'
chdir(moduleDir)

import hpotter_api.test.test_schema as test_schema
from hpotter_api.test.createDb import create_database

if __name__ == '__main__':
    create_database()
    suite = unittest.TestLoader().loadTestsFromModule(test_schema)
    unittest.TextTestRunner().run(suite)
    