from unittest import TestCase

from osbot_jira.api.graph.GS_Graph import GS_Graph
from osbot_utils.utils.Dev import Dev

from osbot_jira.api.graph.Graph_Commands.Graph_Filters import Graph_Filters


class Test_Nodes(TestCase):

    def setUp(self):
        self.filters = Graph_Filters()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_only_with_issue_types(self):
        graph_name = 'graph_9G8'
        issue_type = 'People'
        self.filters.only_with_issue_types('T7F3AUXGV', 'DDKUZTK6X', [graph_name,issue_type])

    def test_only_show_issue_types(self):
        graph_name = 'graph_9G8'
        #graph_name = 'graph_0XM'
        issue_type = 'Risk,People'
        graph : GS_Graph = self.filters.only_show_issue_types(params=[graph_name,issue_type])
        graph.render_puml_and_save_tmp()


    def test_only_link_types(self):
        graph_name = 'graph_XTK'
        link_types = 'has RISK'
        graph: GS_Graph = self.filters.only_with_link_types(params=[graph_name,link_types])
        graph.render_puml_and_save_tmp()

    def test_only_with_field_equal_to(self):
        graph_name = 'graph_XTK'
        field      = 'Rating'
        ratings    = 'Medium'
        graph: GS_Graph = self.filters.only_with_field_equal_to(params=[graph_name, field, ratings])
        self.result = graph.nodes__ratings()
        graph.render_puml_and_save_tmp()

    def test_remove_issue_types(self):
        graph_name = 'graph_9G8'
        issue_type = 'Risk'
        graph = self.filters.remove_issue_types(params=[graph_name,issue_type])
        graph.render_puml_and_save_tmp()

    def test_remove_link_types(self):
        graph_name = 'graph_XTK'
        link_types = 'has RISK,is child of'
        graph = self.filters.remove_link_types(params= [graph_name, link_types])
        graph.render_puml_and_save_tmp()


    def test_only_links_between_nodes(self):
        #graph_name = 'graph_XGV'
        graph_name = 'graph_9G8'
        graph = self.filters.only_links_between_nodes(params=[graph_name])
        assert len(sorted(graph.nodes)) == 17
        #graph.render_puml_and_save_tmp()


    def test_group_by_field(self):
        graph_name = 'graph_XTK'
        #field_name = 'Issue Type'
        field_name = 'Rating'
        #field_name = 'Assignee'
        graph = self.filters.group_by_field(params=[graph_name,field_name])
        graph.render_puml_and_save_tmp()

    def test_group_by_field__issue_links(self):
        graph_name  = 'graph_ZS9'
        field_name  = 'Issue Links'
        #field_name = 'Status'
        graph       = self.filters.group_by_field(params=[graph_name, field_name],)
        graph.render_puml_and_save_tmp()
        # if graph:
        #     graph_name = Graph_Filters._save_graph(graph)
        #     params = ['viva_graph', graph_name, 'default']
        #     png_data = Lambda('lambdas.browser.lambda_browser').invoke({"params": params, 'data': {}})
        #     Dev.pprint(png_data)
        #     Browser_Lamdba_Helper.save_png_data(png_data)
        #
        #     Dev.pprint("Graph Name: {0} image size {1}".format(graph_name, len(png_data)))

 #       Dev.pprint(result.edges)FN

    def test_search_by_field(self):
        graph_name = 'graph_XTK'
        field_name = 'Issue Type'
        value      = 'People'
        field_name = 'Summary'
        value      = 'Jira '
        graph = self.filters.search_by_field(params=[graph_name, field_name, "=", value])
        graph = self.filters.search_by_field(params=[graph_name, field_name, "~", value])
        graph.render_puml_and_save_tmp()
        #Dev.pprint(graph.nodes)
        #Dev.pprint(graph.edges)
        #Dev.pprint(self.filters.search_by_field(params=[graph_name, field_name, "!", value]))


    def test_remove_nodes_with_links(self):
        graph_name = 'graph_XTK'
        self.filters.remove_nodes_with_links(params=[graph_name])


    #Bugs




    def test_fixed_bug_throws_error(self):
        graph_name = 'graph_3RL'
        field_name = 'Status'
        result = self.filters.group_by_field(None, None, [graph_name, field_name])
        Dev.pprint(result)
