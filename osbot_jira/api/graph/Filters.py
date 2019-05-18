from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph


class Filters:

    def __init__(self):
        self.graph                       = None
        self._lambda_graph :Lambda_Graph = None

    def lambda_graph(self):
        if self._lambda_graph is None:
            self._lambda_graph = Lambda_Graph()
        return  self._lambda_graph

    def setup(self,graph=None, graph_name=None):
        if graph_name:
            self.graph = self.lambda_graph().load_gs_graph(graph)
        else:
            self.graph = graph
        return self

    def only_with_issue_types(self, issue_types):
        new_nodes = []
        new_edges = []
        issues = self.graph.get_nodes_issues()
        for key, issue in issues.items():
            if issue:
                issue_type = issue.get('Issue Type')
                if issue_type in issue_types:
                    new_nodes.append(key)

        for edge in self.graph.edges:
            from_key = edge[0]
            to_key = edge[2]
            if from_key in new_nodes and to_key in new_nodes:
                new_edges.append(edge)

        self.graph.set_nodes(new_nodes).set_edges(new_edges)


