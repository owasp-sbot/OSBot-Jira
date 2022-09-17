from osbot_jira.api.graph.Jira_Graph import Jira_Graph


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

    def graph_expand(self, depth) -> Jira_Graph:
        self.jira_graph.add_all_linked_issues(depth=depth)
        #self.jira_graph.get_nodes_issues()                 # see if we need to do this
        return self.jira_graph