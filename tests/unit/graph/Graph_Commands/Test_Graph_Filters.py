from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.api.graph.Graph_Commands.Graph_Filters import Graph_Filters


class Test_Nodes(TestCase):

    def setUp(self):
        self.filters = Graph_Filters()

    def test_remove_link_types(self):
        graph_name = 'graph_XTK'
        link_types = 'has RISK'
        self.filters.remove_link_types('T7F3AUXGV', 'DDKUZTK6X', [graph_name, link_types])

    def test_only_with_issue_types(self):
        graph_name = 'graph_9G8'
        issue_type = 'Risk'
        self.filters.only_with_issue_types('T7F3AUXGV', 'DDKUZTK6X', [graph_name,issue_type])

    def test_only_show_issue_types(self):
        graph_name = 'graph_9G8'
        graph_name = 'graph_0XM'
        issue_type = 'Risk,Vulnerability'
        self.filters.only_show_issue_types('T7F3AUXGV', 'DDKUZTK6X', [graph_name,issue_type])

    def test_only_link_types(self):
        graph_name = 'graph_XTK'
        link_types = 'has RISK'
        self.filters.only_with_link_types('T7F3AUXGV', 'DDKUZTK6X', [graph_name,link_types])

    def test_remove_issue_types(self):
        graph_name = 'graph_9G8'
        issue_type = 'Risk'
        self.filters.remove_issue_types('T7F3AUXGV', 'DDKUZTK6X', [graph_name,issue_type])

    def test_only_links_between_nodes(self):
        graph_name = 'graph_XGV'
        #graph_name = 'graph_XKW'
        graph = self.filters.only_links_between_nodes(params=[graph_name])
        Dev.pprint(len(sorted(graph.edges)))

    def test_group_by_field(self):
        graph_name = 'graph_XTK'
        field_name = 'Issue Type'
        #field_name = 'Rating'
        #field_name = 'Assignee'
        result = self.filters.group_by_field(params=[graph_name,'Issue','Type'])
        Dev.pprint(result.nodes)
        Dev.pprint(result.edges)

    def test_group_by_field__issue_links(self):
        graph_name  = 'graph_ZS9'
        field_name  = 'Issue Links'
        #field_name = 'Status'
        graph       = self.filters.group_by_field('T7F3AUXGV', 'DDKUZTK6X', params=[graph_name, field_name],)
        Dev.pprint(graph)
        if graph:
            graph_name = Graph_Filters._save_graph(graph)
            params = ['viva_graph', graph_name, 'default']
            png_data = Lambda('lambdas.browser.lambda_browser').invoke({"params": params, 'data': {}})
            Dev.pprint(png_data)
            Browser_Lamdba_Helper.save_png_data(png_data)

            Dev.pprint("Graph Name: {0} image size {1}".format(graph_name, len(png_data)))

 #       Dev.pprint(result.edges)FN

    def test_search_by_field(self):
        graph_name = 'graph_XTK'
        field_name = 'Issue Type'
        value      = 'People'
        field_name = 'Summary'
        value      = 'Jira '
        graph = self.filters.search_by_field(params=[graph_name, field_name, "=", value])
        graph = self.filters.search_by_field(params=[graph_name, field_name, "~", value])
        Dev.pprint(graph.nodes)
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
