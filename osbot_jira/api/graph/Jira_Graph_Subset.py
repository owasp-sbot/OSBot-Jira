class Jira_Graph_Subset:

    def __init__(self, jira_graph):
        self.jira_graph          = jira_graph
        self.jira_graph_jql      = None


    def create(self):
        from osbot_jira.api.graph.Jira_Graph_Jql import Jira_Graph_Jql  # to deal with circular dependencies

        nodes_issues        = self.jira_graph.get_nodes_issues()
        self.jira_graph_jql = Jira_Graph_Jql()
        with self.jira_graph_jql as _:
            _.set_issues            (nodes_issues)
            _.set_enable_jira_calls (False       )
            _.set_only_link_if_issue(True        )
        return self

    def render(self, root_key, link_types=None, depth=1):
        with self.jira_graph_jql as _:
            _.set_link_types   (link_types)
            _.set_depth        (depth   )
            _.add_node         (root_key)
            _.render_jira_graph()
        return self

    def create_png(self):
        self.jira_graph_jql.create_jira_graph_png()
        return self

    def render_and_create_png(self, root_key, link_types=None,depth=1):
        self.render(root_key=root_key, link_types=link_types, depth=depth)
        self.create_png()
        return self
