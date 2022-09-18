from unittest import TestCase

from osbot_jira.api.graph.Jira_Graph import create_jira_graph
from osbot_jira.api.graph.Jira_Graph_View import Jira_Graph_View
from osbot_utils.utils.Dev import pprint


class test_Jira_Graph_View(TestCase):

    def setUp(self) -> None:
        Setup()
        #self.jira_graph_view = Jira_Graph_View()
        pass


    def test_view_schema(self):
        root_node       = 'ENTITY-2'                                            # start node
        depth           = 2                                                    # how many levels to expand the graph
        graph           = create_jira_graph(root_node=root_node, depth=depth)   # create graph (i.e. get data from Jira and map Nodes and Edges)
        #pprint(graph.issues.get('ENTITY-2'))


        jira_graph_view = Jira_Graph_View(jira_graph=graph)
        result          = jira_graph_view.view_schema()
        print(jira_graph_view.graph.get_puml())

        jira_graph_view.graph.render_puml_and_save_tmp(use_lambda=False)
        #pprint(result)