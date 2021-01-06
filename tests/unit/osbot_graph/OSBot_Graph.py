from unittest import TestCase

from osbot_jira.osbot_graph.Graph import Graph
from osbot_utils.utils.Dev import Dev


class test_Graph(TestCase):

    def setUp(self):
        self.graph = Graph()
        self.result = None

    def tearDown(self) -> None:
        if self.result is not None:
            Dev.pprint(self.result)

    def test_add_edges(self):
        assert self.graph.add_edges([('a','b')]).edges() == [{'from': 'a', 'label': None, 'to': 'b'}]
        assert self.graph.add_edges([('a', 'b'), ('a','b','c')]).edges() == [ {'from': 'a', 'label': None, 'to': 'b'},
                                                                              {'from': 'a', 'label': 'b' , 'to': 'c'}]

    def test_edges(self):
        self.graph.add_edge_with_label('key_1', 'an label','key_2')
        self.graph.add_edge('key_1', 'key_2', params={'a': 42})
        assert self.graph._edges == { 'key_1__None__key_2'    : { 'from': 'key_1', 'label': None      ,'to': 'key_2','params': {'a': 42 }},
                                      'key_1__an label__key_2': { 'from': 'key_1', 'label': 'an label','to': 'key_2'                    }}

        assert self.graph.edges() == [ {'from': 'key_1', 'label': 'an label', 'to': 'key_2'},
                                       {'from': 'key_1', 'label': None      , 'to': 'key_2' , 'params': {'a': 42} }]

        assert self.graph.edges(group_by='from') == { 'key_1': [ {'from': 'key_1', 'label': 'an label', 'to': 'key_2'},
                                                    { 'from': 'key_1','label': None,'params': {'a': 42},'to': 'key_2'}]}


    def test_nodes(self):
        self.graph.add_node('key_1')
        self.graph.add_node('key_2', 'an value')
        self.graph.add_node('key_3', {'a:':'an value'})

        assert self.graph._nodes == { 'key_1': {'key': 'key_1'   , 'value': 'key_1'                     },
                                      'key_2': {'key': 'key_2'   , 'value': 'an value'                  },
                                      'key_3': {'a:' : 'an value', 'value': 'key_3'   , 'key'  : 'key_3'}}

        assert self.graph.nodes() == [ {'key': 'key_1'   , 'value': 'key_1'                  },
                                       {'key': 'key_2'   , 'value': 'an value'               },
                                       {'a:' : 'an value', 'key'  : 'key_3', 'value': 'key_3'}]

        assert self.graph.nodes(index_by='key') == self.graph._nodes



