from osbot_jira.api.graph.Jira_Graph import Jira_Graph


class Jira_Graph_Query:

    def __init__(self, jira_graph: Jira_Graph):
        self.jira_graph = jira_graph


    def edges(self):
        return self.jira_graph.edges

    def edges_by_link_type(self, link_type=None):
        result = {}
        for (from_id, edge_link_type, to_id) in self.edges():
            if result.get(edge_link_type) is None:
                result[edge_link_type] = []
            result[edge_link_type].append((from_id, to_id ))
        if link_type:
            return result.get(link_type,[])
        return result

    def edges_from_id(self, id):
        result = {}
        for (from_id, link_type, to_id) in self.edges():
            if from_id == id:
                if result.get(link_type) is None:
                    result[link_type] = []
                result[link_type].append(to_id)
        return result

    def nodes(self):
        return self.jira_graph.nodes

    def nodes_adjacent_to_ids(self):
        result = {}
        for (from_id, _, to_id) in self.edges():
            if result.get(from_id) is None:
                result[from_id] = []
            if result.get(to_id) is None:
                result[to_id] = []
            result[from_id].append(to_id)
        return result

    def nodes_issues(self):
        return self.jira_graph.get_nodes_issues()

    def nodes_find(self, queries):
        result = {}
        for node, issue in self.nodes_issues().items():
            match = False
            for key,value in queries.items():
                if (type(value) is list and issue.get(key) in value) or issue.get(key) == value:
                    match = True
                else:
                    match = False
                    break
            if match:
                result[node] = issue
        return result
    def nodes_from_project(self, value, field='Project'):
        matches = []
        for node, issue in self.nodes_issues().items():
            project = issue.get(field)
            if project == value:
                matches.append(node)
        return matches

    def nodes_with_no_adjacent_to_ids(self):
        result = []
        for to_id, adjacent_ids in self.nodes_adjacent_to_ids().items():
            if len(adjacent_ids) == 0:
                result.append(to_id)
        return result

    def nodes_with_adjacent_to_ids(self):
        result = []
        for to_id, adjacent_ids in self.nodes_adjacent_to_ids().items():
            if len(adjacent_ids) > 0:
                result.append(to_id)
        return result
