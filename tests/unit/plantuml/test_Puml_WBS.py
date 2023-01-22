from unittest import TestCase

import networkx
from osbot_plotly.network_graphs.Network_Graph_For_Jira_Graph import Network_Graph_For_Jira_Graph
from osbot_jira.api.graph.Jira_Graph_Jql import Jira_Graph_Jql
from osbot_jira.api.plantuml.Puml_WBS import Puml_WBS
from osbot_utils.utils.Dev import pprint


class test_Puml_WBS(TestCase):

    def setUp(self) -> None:
        self.puml_wbs = Puml_WBS()

    def tearDown(self) -> None:
        (
        #    self.puml_wbs.save_tmp(use_lambda=False)
        )
        #pprint(self.puml_wbs.puml)

    def test_first(self):

        jira_graph_jql = Jira_Graph_Jql().use_cache(True).disable_jira_requests()
        jira_graph_jql.jira_graph.add_node('asd')
        jira_graph_jql.jira_graph.add_edge('asd', 'to', 'top')
        jira_graph_jql.jira_graph.add_edge('top' , 'to', 'AAA')
        jira_graph_jql.jira_graph.add_edge('AAA', 'to', 'BBB')
        jira_graph_jql.jira_graph.add_edge('AAA', 'to', 'CCC')
        jira_graph_jql.jira_graph.add_edge('CCC', 'to', 'DDD')
        # jira_graph_jql.jira_graph.add_edge('CCC', 'to', 'EEE')
        #jira_graph_jql.jira_graph.add_edge('top', 'to', 'BBB')
        network_graph  = Network_Graph_For_Jira_Graph(jira_graph_jql)



        nx_graph = network_graph.nx_graph

        from networkx.readwrite import json_graph
        #pprint(json_graph.tree_data(nx_graph, root='asd'))

        # print()
        # print(networkx.is_tree(nx_graph))
        # print(networkx.is_forest(nx_graph))


        #return
        g = networkx.Graph()
        g.add_node('A')
        g.add_node('B')
        pprint(networkx.is_tree(g))
        network_graph.set_node_text_field('Summary')
        network_graph.show_nodes_and_edges_text(True)
        #network_graph.plotly_network_graph.show_nodes_markers = False
        #network_graph.plotly_network_graph.show_nodes_texts = False
        network_graph.plotly_network_graph.pl_edge_text_size = 10
        network_graph.plotly_network_graph.nx_spring_layout_iterations=1000
        network_graph.plotly_network_graph.show_edges_arrows  = True
        network_graph.plotly_network_graph.pl_edge_line_width = 1
        network_graph.plotly_network_graph.pl_edge_line_color = 'green'
        #network_graph.plotly_network_graph.show

        network_graph.set_title('ABC')
        network_graph.create_networkx_graph()
        network_graph.create_jpg_from_graph()

        self.puml_wbs.puml += """@startwbs
* Business Process Modelling WBS
** Launch the project
*** Complete Stakeholder Research
*** Initial Implementation Plan
** Design phase
*** Model of AsIs Processes Completed
**** Model of AsIs Processes Completed1
**** Model of AsIs Processes Completed2
*** Measure AsIs performance metrics
*** Identify Quick Wins
** Complete innovate phase
@endwbs"""
