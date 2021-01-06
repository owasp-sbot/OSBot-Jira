from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_graphsv.demo.Demo_Data import Demo_Data


class test_Links(TestCase):
    def setUp(self):
        self.demo_data = Demo_Data()
        self.links     = self.demo_data.graph_sv.links
        self.result    = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_all(self):
        self.result = self.links.all()

    def test_add(self):
        assert self.links.add('a','to','b') == {'data': "link added: ['a', 'to', 'b']", 'status': 'ok'}
        assert self.links.delete('a', 'to', 'b') == {'data': "link deleted: ['a', 'to', 'b']", 'status': 'ok'}

