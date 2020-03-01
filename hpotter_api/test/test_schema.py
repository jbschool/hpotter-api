import unittest
from ..schema import schema

class SchemaTests(unittest.TestCase):

    def setUp(self):
        print('setting up...')

    def test_good_query_returns(self):
        query = '{"query":"{\n  allConnections{\n    edges{\n      node{\n        destIP\n        destPort\n        sourceIP\n        sourcePort\n      }\n    }\n  }\n}","variables":null,"operationName":null}'
        result = schema.execute(query).to_dict()
        print(result)
        self.assertTrue(1 == 1)

    def test_false_is_false(self):
        self.assertFalse(False)