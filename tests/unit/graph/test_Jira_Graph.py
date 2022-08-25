from unittest import TestCase

from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_utils.utils.Dev import pprint


class Test_GS_Graph(TestCase):

    def setUp(self):
        self.graph  = Jira_Graph()
        #self.result = None

    # def tearDown(self):
    #     if self.result is not None:
    #         pprint(self.result)

    def test_ctor(self):
        pprint(self.graph.puml_options)

    def test_add_node(self):
        self.graph.add_node('a')
        assert self.graph.nodes == ['a']

    def test_graph(self):
        graph = self.graph.add_node('aaa').graph()
        assert graph.nodes == [{'key': 'aaa', 'label': 'aaa'}]