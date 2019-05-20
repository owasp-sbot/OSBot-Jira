import json
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Local_Cache import use_local_cache_if_available, save_result_to_local_cache

from osbot_jira.api.graph.Filters import Filters
from osbot_jira.api.graph.GS_Graph import GS_Graph


class test_Filters(TestCase):

    def setUp(self):
        self.graph = GS_Graph()
        self.filters = Filters()
        self.result  = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    # helper methods

    @use_local_cache_if_available
    #@save_result_to_local_cache
    def get_graph_json(self,graph_name):
        return self.filters.lambda_graph().load_gs_graph(graph_name).to_json(store_issues=True)

    def get_graph(self,graph_name):
        graph_json : str      = self.get_graph_json(graph_name)
        graph      : GS_Graph = GS_Graph().from_json(graph_json)
        return graph

    def use_graph(self,graph_name):
        graph = self.get_graph(graph_name)
        return self.filters.setup(graph=graph)

    def show_graph(self):
        self.filters.graph.render_puml_and_save_tmp()

    # class methods
    def test__init__(self):
        assert self.filters.graph is None

    def test_only_with_issue_types(self):
        graph_name  = 'graph_9G8'
        issue_types = ['Risk']
        graph = self.get_graph(graph_name)

        assert sorted(graph.issues__issue_types()) == ['Business entity', 'IT Asset', 'People', 'Risk']
        self.filters.setup(graph=graph).only_with_issue_types(issue_types)
        assert graph.issues__issue_types() == ['Risk']

        #self.result = graph.render_puml_and_save_tmp()

    def test_only_show_issue_types(self):
        graph_name = 'graph_9G8'
        issue_types = ['People']
        graph = self.get_graph(graph_name)
        self.filters.setup(graph=graph).only_show_issue_types(issue_types)

    def test_only_link_types(self):
        graph_name = 'graph_XTK'
        link_types = ['has RISK']
        graph = self.get_graph(graph_name)
        assert graph.edges__link_types() == [ 'has Business Owner', 'has RISK', 'has Technical Owner', 'is child of', 'is managed by']
        self.filters.setup(graph=graph).only_with_link_types(link_types)
        assert graph.edges__link_types() == link_types

    def test_only_with_field_equal_to(self):
        graph_name = 'graph_9G8'
        field      = 'Issue Type'
        values     = ['People']
        graph      = self.get_graph(graph_name)
        self.result = graph.nodes__field_values('Issue Type')
        assert graph.nodes__field_values('Issue Type') == ['Business entity', 'IT Asset', 'People', 'Risk']
        self.filters.setup(graph=graph).only_with_field_equal_to(field, values)
        assert graph.nodes__field_values('Issue Type') == values

    def test_only_links_between_nodes(self):
        self.use_graph('graph_9G8').only_links_between_nodes()
        assert self.filters.graph.edges__link_types() == [ 'RISK affects', 'has Business Owner', 'has RISK', 'has Technical Owner', 'is Business Owner', 'is Technical Owner', 'is child of', 'is managed by', 'is manager of', 'is parent of']
        #self.show_graph()

