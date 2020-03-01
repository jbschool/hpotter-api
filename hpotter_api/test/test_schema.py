import unittest
from json import loads, dumps

from ..schema import schema

class SchemaTests(unittest.TestCase):

    def test_good_query_returns(self):
        postBody = r'{"query":"{\n  allConnections{\n    edges{\n      node{\n        destIP\n        destPort\n        sourceIP\n        sourcePort\n      }\n    }\n  }\n}","variables":null,"operationName":null}'
        query = loads(postBody)['query']
        result = schema.execute(query).to_dict()

        data = result.get('data')
        self.assertIsNotNone(data)
        allConnections = data.get('allConnections')
        self.assertIsNotNone(allConnections)
        edges = allConnections.get('edges')
        self.assertIsNotNone(edges)
        self.assertTrue(len(edges) == 2)