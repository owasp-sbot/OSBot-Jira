from unittest import TestCase

from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set


class Test_GS_Graph(TestCase):

    def setUp(self):
        self.graph  = Jira_Graph()

        self.root_node = 'CSF-38'
        #self.result = None

    # def tearDown(self):
    #     if self.result is not None:
    #         pprint(self.result)

    def test_ctor(self):
        assert self.graph.puml_options == { 'height'              : None     ,
                                            'left-to-right'       : True     ,
                                            'link-types-to-add'   : []       ,
                                            #'link-types-to-ignore': []       ,
                                            'node-text-value'     : 'Summary',
                                            #'only-from-projects'  : []       ,
                                            'show-edge-labels'    : True     ,
                                            'show-key-in-text'    : True     ,
                                            'width'               : None     }

    def test_add_issue(self):
        assert self.graph.issues is None
        self.graph.add_issue('key', {'an':'issue'})
        assert self.graph.issues == {'key': {'an': 'issue'}}

    def test_add_node(self):
        self.graph.add_node('a')
        assert self.graph.nodes == ['a']

    def test_add_nodes(self):
        self.graph.add_nodes(['a','b','c'])
        assert self.graph.nodes == ['a', 'b', 'c']

    def test_add_edge(self):
        assert self.graph.nodes == []
        assert self.graph.edges == []
        self.graph.add_edge('from_key', 'link_type', 'to_key')
        assert self.graph.nodes == []
        assert self.graph.edges == [('from_key', 'link_type', 'to_key')]

    def test_add_edges(self):
        self.graph.add_edges((('from_key_1', 'link_type', 'to_key'), ('from_key_2', 'link_type', 'to_key')))
        self.graph.add_edges([('from_key_3', 'link_type', 'to_key'), ('from_key_4', 'link_type', 'to_key')])
        assert self.graph.nodes == []
        assert self.graph.edges == [ ('from_key_1', 'link_type', 'to_key'),
                                     ('from_key_2', 'link_type', 'to_key'),
                                     ('from_key_3', 'link_type', 'to_key'),
                                     ('from_key_4', 'link_type', 'to_key')]

    # this is using live data from a Jira instance todo: add enough test data that this is not needed
    def test_add_all_linked_issues(self):
        #self.create_test_graph()               # todo: once this is working refactor code to use test data
        depth    = 3
        self.graph.add_node(self.root_node)
        self.graph.add_all_linked_issues(depth=depth)
        assert len(self.graph.nodes) > 200
        assert len(self.graph.edges) > 300



    def test_graph(self):
        self.graph.add_node('aaa').add_node('bbb').add_edge('aaa', 'test_link', 'bbb')

        graph = self.graph.graph()
        pprint(graph.nodes())
        assert graph.nodes() == [{'key': 'aaa', 'label': 'aaa'},
                                 {'key': 'bbb', 'label': 'bbb'}]
        assert graph.edges() == [{'from': 'aaa', 'label': 'test_link', 'to': 'bbb'}]

    def test_jira_get_link_types_per_key_for_issues(self):
        # self.create_test_graph()               # todo: once this is working refactor code to use test data
        self.graph.add_node(self.root_node)
        result = self.graph.jira_get_link_types_per_key_for_issues()
        assert list_set(result.get(self.root_node)) == ['has NIST category', 'is NIST category of']

    def test_jira__jira_get_issue_link_types_per_key_for_issues__indexed_by_to_key(self):
        self.graph.add_node(self.root_node)
        result = self.graph.jira_get_issue_link_types_per_key_for_issues__indexed_by_to_key()
        assert result.get('CSF-1') == {'has NIST CSF category': [self.root_node]}
