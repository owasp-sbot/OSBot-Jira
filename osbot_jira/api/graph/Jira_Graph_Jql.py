from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_jira.api.graph.Jira_Graph_View import Jira_Graph_View


class Jira_Graph_Jql:

    #def __init__(self, root_node, initial_nodes, issue_links=None, skin_params=None):
    def __init__(self, jql):
        self.jira_graph = Jira_Graph()
        self.api_jira   = self.jira_graph.api_jira
        self.jql        = jql
        self.jql_keys   = []
        # if root_node:
        #     self.jira_graph.add_node(root_node)
        # if initial_nodes:
        #     self.jira_graph.add_nodes(initial_nodes)
        # if issue_links:
        #     self.jira_graph.set_puml_link_types_to_add(issue_links)
        # if skin_params:
        #     self.jira_graph.set_skin_params(issue_links)

    def execute_jql(self):
        if self.jql:
            self.jql_keys = self.api_jira.search__return_keys(jql=self.jql)
            self.jira_graph.add_nodes(self.jql_keys)
        return self

    def graph_expand(self, depth):
        self.jira_graph.add_all_linked_issues(depth=depth)
        #self.jira_graph.get_nodes_issues()                 # see if we need to do this
        return self

    def render_png(self):
        return self.jira_graph.render_puml_and_save_tmp(use_lambda=False)

    def render_png__schema(self):
        jira_graph_view = Jira_Graph_View(jira_graph=self.jira_graph)
        schema_graph = jira_graph_view.create_schema_graph()
        #schema_graph.set_puml_left_to_right(False)
        schema_graph.set_skin_param('linetype', 'polyline')
        #schema_graph.set_skin_param('linetype', 'ortho')
        schema_graph.render_puml_and_save_tmp(use_lambda=False)
        return schema_graph

