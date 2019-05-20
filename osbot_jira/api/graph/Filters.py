from pbx_gs_python_utils.utils.Misc    import Misc
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


    def group_by_field(self, root_node, field_name):
        graph       = self.graph
        issues      = graph.get_nodes_issues()  # resolve current node's issues
        nodes       = graph.nodes               # save current nodes
        edges       = graph.edges               # save current edges
        graph.nodes = []                        # reset nodes
        graph.edges = []                        # reset edges
        graph.add_node(root_node)
        if field_name == 'Issue Links':
            for edge in edges:
                link_type = edge[1]
                to_key    = edge[2]
                to_issue = Misc.get_value(issues, to_key, {})
                to_key   = Misc.get_value(to_issue, 'Key')
                graph.add_node(link_type)
                graph.add_node(to_key)
                graph.add_edge(root_node, '', link_type)
                graph.add_edge(link_type, '', to_key)

        else:
            for node in nodes:
                issue = issues.get(node)
                if issue:
                    value = issue.get(field_name)
                    graph.add_node(value)
                    graph.add_node(node)
                    graph.add_edge(root_node, field_name, value)
                    graph.add_edge(value, '', node)
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
        issues = self.graph.get_nodes_issues().items()
        for key, issue in issues:
            if issue:
                issue_links = issue.get('Issue Links')          # get all links for issue
                for issue_link, targets in issue_links.items():
                    for target in targets:
                        if key in self.graph.nodes and target in self.graph.nodes:
                            self.graph.add_edge(key, issue_link, target)
        return self


    def remove_field_equal_to(self,field_name, issue_types):
        new_nodes = []
        new_edges = []
        issues = self.graph.get_nodes_issues()
        for key, issue in issues.items():
            issue_type = issue.get(field_name)
            if issue_type not in issue_types:
                new_nodes.append(key)

        for edge in self.graph.edges:
            from_key = edge[0]
            to_key   = edge[2]
            if from_key in new_nodes and to_key in new_nodes:
                new_edges.append(edge)

        self.graph.set_nodes(new_nodes)             \
                  .set_edges(new_edges)
        return self

    def remove_link_types(self, link_types):
        new_edges = []                                                                              # array to hold the new edges
        for index,edge in enumerate(self.graph.edges):                                              # for each edge
            link_type = edge[1]                                                                     # get link_type from edge triplet: (from_node, link_type, to_node)
            if link_type not in link_types:                                                         # if link_type is NOT in the params passed
                new_edges.append(edge)                                                              # add edge from new_edges array
        self.graph.set_edges(new_edges).remove_no_links()                                           # update original graph with new edges and remove nodes with no links
        return

    def remove_nodes_with_issue_types(self, issue_types):
        return self.remove_field_equal_to('Issue Type', issue_types)

    def remove_nodes_from_projects(self, projects):
        return self.remove_field_equal_to('Project', projects)

    def search_by_field__contains(self, field_name, value_to_find):
        return self.search_by_field(field_name, 'contains', value_to_find)

    def search_by_field__equals(self, field_name, value_to_find):
        return self.search_by_field(field_name, 'equals', value_to_find)

    def search_by_field__not_contains(self, field_name, value_to_find):
        return self.search_by_field(field_name, 'not contains', value_to_find)

    def search_by_field__not_equals(self, field_name, value_to_find):
        return self.search_by_field(field_name, 'not equals', value_to_find)

    def search_by_field(self,field_name, search_type, value_to_find):
        issues  = self.graph.get_nodes_issues()
        results = []
        for key, issue in issues.items():
            issue_value = issue.get(field_name)
            if issue_value:
                if search_type == 'contains':
                    if value_to_find.lower() in issue_value.lower().strip():
                        results.append(key)
                if search_type == 'equals':
                    if value_to_find.lower() == issue_value.lower().strip():
                        results.append(key)
                if search_type == 'not contains':
                    if value_to_find.lower() not in issue_value.lower().strip():
                        results.append(key)
                if search_type == 'not equals':
                    if value_to_find.lower() != issue_value.lower().strip():
                        results.append(key)

        self.graph.set_nodes(results)
        self.only_edges_with_both_nodes()
        return self