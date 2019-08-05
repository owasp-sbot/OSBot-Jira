from osbot_jira.api.graph.GS_Graph import GS_Graph


class GS_Graph_SV(GS_Graph):

    def __init__(self, graph_sv):
        self.graph_sv = graph_sv
        super().__init__()

    def all_link_types(self):
        return self.graph_sv.indexes.by_link_types()

    def get_nodes_issues(self):
        issues_by_key = self.graph_sv.indexes.by_key()
        issues = {}
        for issue_key in self.nodes:
            issue_data = issues_by_key.get(issue_key)
            if issue_data:
                issues[issue_key] = issue_data.get('data')
        return issues