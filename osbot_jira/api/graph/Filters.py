from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph


class Filters:

    def __init__(self):
        self.graph                       = None
        self._lambda_graph :Lambda_Graph = None

    def lambda_graph(self):
        if self._lambda_graph is None:
            self._lambda_graph = Lambda_Graph()
        return  self._lambda_graph

    def setup(self, graph=None, graph_name=None):
        if graph_name:
            self.graph = self.lambda_graph().load_gs_graph(graph_name)
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
        return self

    def only_show_issue_types(self,issue_types):
        new_nodes = []
        issues = self.graph.get_nodes_issues()
        for key, issue in issues.items():
            if issue:
                issue_type = issue.get('Issue Type')
                if issue_type in issue_types:
                    new_nodes.append(key)

        self.graph.set_nodes(new_nodes)             # this version as an interesting side effect since we are not removing the edges with no nodes
        return self

    def only_with_link_types(self, link_types):
        new_edges = []
        for index, edge in enumerate(self.graph.edges):
            link_type = edge[1]
            if link_type in link_types:
                new_edges.append(edge)
        self.graph.set_edges(new_edges).remove_no_links()
        return self

    def only_with_field_equal_to(self,field, values):
        new_nodes = []
        issues = self.graph.get_nodes_issues()
        for key, issue in issues.items():
            issue_type = issue.get(field)
            if issue_type in values:
                new_nodes.append(key)
        self.graph.set_nodes(new_nodes)      # this version as an interesting side effect since we are not removing the edges with no nodes
        self.only_edges_with_both_nodes()    # remove edges that don't have both links
        return self


    def only_edges_with_both_nodes(self):
        new_edges = []
        nodes = self.graph.nodes
        for edge in list(self.graph.edges):
            if edge[0] in nodes and edge[2] in nodes:  # if both edges exist in the current list of nodes
                new_edges.append(edge)  # keep the edge
        self.graph.edges = new_edges
        return self


    def only_links_between_nodes(self):
        """
        this filter will replace all edges with all links between the current nodes
        """
        self.graph.edges = []                                   # clear all edges from graph
        new_nodes        =  []
        issues = self.graph.get_nodes_issues().items()
        for key, issue in issues:
            if issue:
                issue_links = issue.get('Issue Links')          # get all links for issue
                for issue_link, targets in issue_links.items():
                    for target in targets:
                        if key in self.graph.nodes and target in self.graph.nodes:
                            self.graph.add_edge(key, issue_link, target)
        return self
