from unittest import TestCase

from osbot_jira.api.graph.Jira_Graph_Jql import Jira_Graph_Jql
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_string


class test_Jira_Graph_Jql(TestCase):

    def setUp(self) -> None:
        self.jql            = 'project=PROJ'
        self.jira_graph_jql = Jira_Graph_Jql(jql=self.jql)
        self.jira_graph     = self.jira_graph_jql.jira_graph

    def test__init__(self):
        assert self.jira_graph_jql.jql == self.jql
        jql = random_string()
        assert Jira_Graph_Jql(jql=jql).jql == jql

    def test_execute_jql(self):
        #valid jql
        self.jira_graph_jql.execute_jql()
        assert len(self.jira_graph_jql.jql_keys) > 0
        assert self.jira_graph_jql.jql_keys == self.jira_graph.nodes

        # empty jql
        jira_graph_jql = Jira_Graph_Jql(jql='')
        jira_graph_jql.execute_jql()
        assert len(jira_graph_jql.jql_keys) == 0
        assert jira_graph_jql.jql_keys      == jira_graph_jql.jira_graph.nodes

        # bad jql
        jira_graph_jql = Jira_Graph_Jql(jql='aa^^&^$%^BB')
        jira_graph_jql.execute_jql()
        assert len(jira_graph_jql.jql_keys) == 0
        assert jira_graph_jql.jql_keys == jira_graph_jql.jira_graph.nodes

    def test_graph_expand__with_node_text_override(self):

        def on_add_node(element,title, id_plant_uml, id_jira):
            title = random_string()
            puml_card = '{0} "{1}" as {2}'.format(element, title, id_plant_uml)
            return puml_card

        depth =4
        self.jira_graph_jql.execute_jql()
        self.jira_graph_jql.jql_keys = self.jira_graph_jql.jql_keys[0:1]
        self.jira_graph.nodes        = self.jira_graph_jql.jql_keys

        self.jira_graph.set_puml_on_add_node(on_add_node)

        self.jira_graph_jql.graph_expand(depth=depth)
        jira_graph = self.jira_graph_jql.jira_graph
        pprint(len(self.jira_graph.nodes))
        pprint(len(self.jira_graph.edges))

        self.jira_graph.render_puml_and_save_tmp(use_lambda=False)

        print(self.jira_graph.get_puml())

