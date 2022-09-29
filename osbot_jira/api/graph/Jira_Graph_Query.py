from osbot_jira.api.graph.Jira_Graph import Jira_Graph


class Jira_Graph_Query:

    def __init__(self, jira_graph: Jira_Graph):
        self.jira_graph = jira_graph


    def nodes(self):
        return self.jira_graph.nodes

    def nodes_issues(self):
        return self.jira_graph.get_nodes_issues()

    def nodes_from_project(self, value, field='Project'):
        matches = []
        for node, issue in self.nodes_issues().items():
            project = issue.get(field)
            if project == value:
                matches.append(node)
        return matches


    def edges(self):
        return self.jira_graph.edges