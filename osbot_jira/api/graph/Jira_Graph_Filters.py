from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_utils.utils import Misc
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set, unique


class Jira_Graph_Filters:

    def __init__(self, jira_graph: Jira_Graph):        
        self.jira_graph = jira_graph

    def colapse_node(self, key, include_from_links=False, include_to_links=True):
        graph = self.jira_graph
        edges_from      = graph.edges_from(key)
        edges_to        = graph.edges_to(key)
        edges_to_add    = []
        edges_to_delete = []
        for edge_from in edges_from:
            (from_id, from_link_type,_) =  edge_from
            edges_to_delete.append(edge_from)
            for edge_to in edges_to:
                (_,to_link_type, to_id) = edge_to
                if include_from_links:
                    edges_to_add.append((from_id, from_link_type, to_id))
                if include_to_links:
                    edges_to_add.append((from_id, to_link_type, to_id))
                edges_to_delete.append(edge_to)
        edges_to_add = unique(edges_to_add)
        graph.add_edges   (edges_to_add   )
        graph.delete_edges(edges_to_delete)
        self.delete_node(key)
        return self

    def colapse_nodes(self, keys, include_from_links=False, include_to_links=True):
        for key in keys:
            self.colapse_node(key, include_from_links=include_from_links, include_to_links=include_to_links)
        return self

    def colapse_nodes_to(self, key):
        nodes_to = self.jira_graph.nodes_to(key)
        for key in nodes_to:
            self.colapse_node(key)
        return self

    def delete_edge(self, edge):
        self.jira_graph.delete_edge(edge)
        return self

    def delete_edges(self, edges):
        self.jira_graph.delete_edges(edges)
        return self

    def delete_node(self,key, delete_edges=False, delete_from_nodes=False, delete_to_nodes=False):
        if key:
            from_nodes = []
            to_nodes   = []
            if key in self.jira_graph.nodes:
                self.jira_graph.nodes.remove(key)
                for edge in list(self.jira_graph.edges):
                    (from_key, _, to_key) = edge
                    if from_key == key or to_key == key:
                        from_nodes.append(from_key)
                        to_nodes  .append(to_key)
                        if delete_edges:
                            self.jira_graph.edges.remove(edge)

            if self.jira_graph.issues and self.jira_graph.issues.get(key) is not None:
                del self.jira_graph.issues[key]

            if delete_from_nodes:
                for from_node in from_nodes:
                    self.delete_node(from_node, delete_edges=delete_edges)

            if delete_to_nodes:
                for to_node in to_nodes:
                    self.delete_node(to_node, delete_edges=delete_edges)

        return self

    # def delete_node(self, node_id):
    #     if node_id in self.jira_graph.nodes:
    #         self.jira_graph.nodes.remove(node_id)
    #         edges_to_remove = []
    #         for edge in self.jira_graph.edges:
    #             (from_id, link_type, to_id) = edge
    #             if node_id == from_id or node_id == to_id:
    #                 edges_to_remove.append(edge)
    #         for edge_to_remove in edges_to_remove:
    #             self.jira_graph.edges.remove(edge_to_remove)
    #     return self

    def delete_nodes(self, nodes_ids,delete_edges=False, delete_from_nodes=False, delete_to_nodes=False):       # todo: refactor into more efficient deletion
        for node_id in nodes_ids:
            self.delete_node(node_id, delete_edges=delete_edges, delete_from_nodes=delete_from_nodes,delete_to_nodes=delete_to_nodes)
        return self

    def delete_nodes_from(self, field, value):
        graph = self.jira_graph
        issues = graph.issues
        nodes_to_delete = []
        for node_id in self.jira_graph.nodes:
            node_issue  = issues.get(node_id, {})
            field_value = node_issue.get(field)
            if field_value == value:
                nodes_to_delete.append(node_id)
        self.delete_nodes(nodes_to_delete)
        return self

    def delete_nodes_with_no_edges(self):
        nodes_to_delete = []
        for node_id in self.jira_graph.nodes:
            found = False
            for (from_id, link_type, to_id) in self.jira_graph.edges:
                if node_id == from_id or node_id == to_id:
                    found = True
                    break
            if found is False:
                nodes_to_delete.append(node_id)
        for node_to_delete in nodes_to_delete:
            #print(node_to_delete)
            self.jira_graph.nodes.remove(node_to_delete)
        return self

    # double check if this is working as expected
    # def delete_edges_with_no_issues(self):
    #     edges_to_delete = []
    #     issues = self.jira_graph.issues
    #     pprint(len(self.jira_graph.edges))
    #     for edge in self.jira_graph.edges:
    #         (from_node, type, to_node) = edge
    #
    #         if issues.get(from_node) is None and issues.get(to_node) is None:
    #             edges_to_delete.append(edge)
    #             #print(from_node)
    #     self.delete_edges(edges_to_delete)
    #     pprint(len(self.jira_graph.edges))
    #     return self

    def expand_edges_with_same__to_id(self, depth = 10):
        for i in range(0,depth):
            graph = self.jira_graph
            issues = graph.issues
            to_ids = {}
            for edge in graph.edges:
                (from_id, _, to_id) = edge
                if to_ids.get(to_id) is None:
                    to_ids[to_id] = []
                to_ids[to_id].append(edge)
            same_to_ids = {}
            for key, edges in to_ids.items():
                if len(edges) > 1:
                    same_to_ids[key] = edges
            new_edges       = []
            new_nodes       = {}
            nodes_to_remove = []

            for key, edges in same_to_ids.items():
                for edge in edges:
                    (from_id, link_type, to_id) = edge
                    new_unique_key = f"{from_id}__{to_id}"
                    issue          = issues.get(to_id)

                    new_nodes[new_unique_key] = issue
                    new_edges.append((from_id       , link_type, new_unique_key))
                    new_edges.append((new_unique_key, link_type, to_id         ))
                    nodes_to_remove.append(to_id)
                    graph.edges.remove(edge)

            for key, issue in new_nodes.items():
                graph.add_node(key, issue)

            graph.edges.extend(new_edges)

            index_by_from_id = {}
            index_by_to_id   = {}
            for edge in graph.edges:
                (from_id, _, to_id) = edge
                if index_by_from_id.get(from_id) is None:
                    index_by_from_id[from_id] = []
                index_by_from_id[from_id].append(edge)

                if index_by_to_id.get(to_id) is None:
                    index_by_to_id[to_id] = []
                index_by_to_id[to_id].append(edge)

            for node_to_remove in unique(nodes_to_remove):
                from_ids_edges = index_by_from_id.get(node_to_remove, [])
                to_ids_edges   = index_by_to_id.get  (node_to_remove, [])

                for from_id_edge in from_ids_edges:
                    (_,link_type, to_id) = from_id_edge
                    for to_id_edge in to_ids_edges:
                        (from_id,_,_) = to_id_edge
                        graph.edges.append((from_id, link_type, to_id))
            self.delete_nodes(nodes_to_remove, delete_edges=True)
        return self

    def group_by_link_type(self):
        graph       = self.jira_graph
        edges       = graph.edges
        new_edges   = []
        edges_by_link_type = {}
        for edge in edges:
            (_, link_type, _) = edge
            if edges_by_link_type.get(link_type) is None:
                edges_by_link_type[link_type] = []
            edges_by_link_type[link_type].append(edge)

        for link_type, edges in edges_by_link_type.items():
            self.jira_graph.add_node(link_type, {})
            for edge in edges:
                (from_id, _, to_id) = edge
                new_edges.append((from_id  , '', link_type))
                new_edges.append((link_type, '', to_id))

        graph.edges = unique(new_edges)
        return self

    def group_by_status(self, only_for_project=None):
        issues = self.jira_graph.issues
        graph  = self.jira_graph
        new_nodes= []
        new_edges = []
        for edge in graph.edges:
            (from_id, _, to_id) = edge
            to_issue = issues.get(to_id, {})
            status   = to_issue.get('Status')
            if only_for_project and only_for_project != to_issue.get('Project'):
                new_edges.append(edge)
            else:
                new_edges.append((from_id, '', status))
                new_edges.append((status , '', to_id))
                new_nodes.append(status)
        graph.edges = unique(new_edges)
        graph.nodes.extend(unique(new_nodes))
        return self

    def group_by_field(self, root_node, field_name):
        graph       = self.jira_graph
        issues      = graph.get_nodes_issues()  # resolve current node's issues     # todo, this will not work with the current mode where have cached all issues in the issues field
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

    def only_nodes_with_edges(self):
        return self.delete_nodes_with_no_edges()

    def only_with_issue_types(self, issue_types):
        if issue_types:
            new_nodes = []
            new_edges = []
            issues = self.jira_graph.get_nodes_issues()
            for key, issue in issues.items():
                if issue:
                    issue_type = issue.get('Issue Type')
                    if issue_type in issue_types:
                        new_nodes.append(key)

            for edge in self.jira_graph.edges:
                from_key = edge[0]
                to_key = edge[2]
                if from_key in new_nodes and to_key in new_nodes:
                    new_edges.append(edge)

            self.jira_graph.set_nodes(new_nodes).set_edges(new_edges)
        return self

    def only_show_issue_types(self,issue_types):
        if issue_types:
            new_nodes = []
            issues = self.jira_graph.get_nodes_issues()
            for key, issue in issues.items():
                if issue:
                    issue_type = issue.get('Issue Type')
                    if issue_type in issue_types:
                        new_nodes.append(key)

            self.jira_graph.set_nodes(new_nodes)             # this version as an interesting side effect since we are not removing the edges with no nodes
        return self

    def only_with_link_types(self, link_types):
        if link_types:
            new_edges = []
            for index, edge in enumerate(self.jira_graph.edges):
                link_type = edge[1]
                if link_type in link_types:
                    new_edges.append(edge)
            self.jira_graph.set_edges(new_edges).remove_no_links()
        return self

    def only_with_field_equal_to(self,field, values):
        if field and values:
            new_nodes = []
            issues = self.jira_graph.get_nodes_issues()
            for key, issue in issues.items():
                field_value = issue.get(field)
                if field_value in values:
                    new_nodes.append(key)
            self.jira_graph.set_nodes(new_nodes)      # this version as an interesting side effect since we are not removing the edges with no nodes
            #self.only_edges_with_both_nodes()    # remove edges that don't have both links
        return self

    def only_with_projects_or_field_equal_to(self, field_name, values, projects_to_keep=None, jira_fields=None):
        if  field_name and values:
            new_nodes = []
            issues = self.jira_graph.get_nodes_issues(reload=True, fields=jira_fields)
            for key, issue in issues.items():
                project = issue.get('Project')
                if projects_to_keep and project in projects_to_keep:
                    new_nodes.append(key)
                    continue
                field_value = issue.get(field_name)
                print(field_value)
                if field_value in values:
                    new_nodes.append(key)
            self.jira_graph.set_nodes(new_nodes)      # this version as an interesting side effect since we are not removing the edges with no nodes
            #self.only_edges_with_both_nodes()    # remove edges that don't have both links
        return self

    def only_nodes_with_no_edges(self):
        nodes_with_edges    = []
        nodes_with_no_edges = []
        for edge in list(self.jira_graph.edges):
            nodes_with_edges.append(edge[0])
            nodes_with_edges.append(edge[2])
        nodes_with_edges = unique(nodes_with_edges)
        for node in self.jira_graph.nodes:
            if node not in nodes_with_edges:
                nodes_with_no_edges.append(node)
        self.jira_graph.nodes = nodes_with_no_edges
        self.jira_graph.edges = []
        return self

    def only_edges_with_both_nodes(self):
        new_edges = []
        nodes = self.jira_graph.nodes
        for edge in list(self.jira_graph.edges):
            if edge[0] in nodes and edge[2] in nodes:  # if both edges exist in the current list of nodes
                new_edges.append(edge)  # keep the edge
        self.jira_graph.edges = new_edges
        return self


    def only_links_between_nodes(self):
        """
        this filter will replace all edges with all links between the current nodes
        """
        self.jira_graph.edges = []                                   # clear all edges from graph
        issues = self.jira_graph.get_nodes_issues().items()
        for key, issue in issues:
            if issue:
                issue_links = issue.get('Issue Links')          # get all links for issue
                for issue_link, targets in issue_links.items():
                    for target in targets:
                        if key in self.jira_graph.nodes and target in self.jira_graph.nodes:
                            self.jira_graph.add_edge(key, issue_link, target)
        return self


    def refactor_link_to_child_links(self, refactor_issue_link, child_issue_link):
        issues = self.jira_graph.get_nodes_issues().items()
        for key, issue in issues:
            if issue:
                issue_links = issue.get('Issue Links')  # get all links for issue
                for issue_link__refactor, targets__refactor in issue_links.items():
                    if refactor_issue_link == issue_link__refactor:
                        for target__refactor in targets__refactor:
                            for issue_link__child, targets__child in issue_links.items():
                                if issue_link__child == child_issue_link:
                                    for target__child in targets__child:
                                        self.jira_graph.add_edge(from_key=target__child, link_type=issue_link__child, to_key=target__refactor)

                            edge_to_delete = (key, refactor_issue_link, target__refactor)
                            self.jira_graph.delete_edge(edge_to_delete)
        return self



    def remove_field_equal_to(self,field_name, issue_types):
        new_nodes = []
        new_edges = []
        issues = self.jira_graph.get_nodes_issues()
        for key, issue in issues.items():
            issue_type = issue.get(field_name)
            if issue_type not in issue_types:
                new_nodes.append(key)

        for edge in self.jira_graph.edges:
            from_key = edge[0]
            to_key   = edge[2]
            if from_key in new_nodes and to_key in new_nodes:
                new_edges.append(edge)

        self.jira_graph.set_nodes(new_nodes)             \
                  .set_edges(new_edges)
        return self

    def remove_link_types(self, link_types):
        new_edges = []                                                                              # array to hold the new edges
        for index,edge in enumerate(self.jira_graph.edges):                                              # for each edge
            link_type = edge[1]                                                                     # get link_type from edge triplet: (from_node, link_type, to_node)
            if link_type not in link_types:                                                         # if link_type is NOT in the params passed
                new_edges.append(edge)                                                              # add edge from new_edges array
        self.jira_graph.set_edges(new_edges).remove_no_links()                                           # update original graph with new edges and remove nodes with no links
        return

    def remove_nodes_with_issue_types(self, issue_types):
        return self.remove_field_equal_to('Issue Type', issue_types)

    #todo: see if this filter still works
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
        issues  = self.jira_graph.get_nodes_issues()
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

        self.jira_graph.set_nodes(results)
        #self.only_edges_with_both_nodes()
        return self