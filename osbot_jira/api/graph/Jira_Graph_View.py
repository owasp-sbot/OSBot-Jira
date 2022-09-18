from osbot_jira.api.graph.Jira_Graph import Jira_Graph


class Jira_Graph_View:

    def __init__(self, jira_graph : Jira_Graph):
        self.jira_graph = jira_graph

    def create_schema_graph(self):
        issues = self.jira_graph.get_nodes_issues(reload=False, fields='issuetype')

        schema = {}
        puml = self.jira_graph.puml
        for edge in self.jira_graph.edges:
            from_id   = edge[0]
            link_name = edge[1]
            to_id     = edge[2]
            if issues[from_id]:
                from_issue_type = puml.fix_id(issues[from_id].get('Issue Type'))
            else:
                from_issue_type = 'NA'

            if issues[to_id]:
                to_issue_type   = puml.fix_id(issues[to_id].get('Issue Type'))
            else:
                to_issue_type = 'NA'
            schema_edge = (from_issue_type,link_name,to_issue_type)
            if schema.get(schema_edge) is None: schema[schema_edge] = { 'count'           : 0               ,
                                                                        'from_issue_type' : from_issue_type ,
                                                                        'link_name'       : link_name       ,
                                                                        'to_issue_type'   : to_issue_type }
            schema.get(schema_edge)['count'] += 1

        schema_graph = Jira_Graph()

        for item in schema.values():
            schema_graph.add_node(item.get('from_issue_type'))
            schema_graph.add_node(item.get('to_issue_type'))
            schema_graph.add_edge(item.get('from_issue_type'), item.get('link_name'),item.get('to_issue_type'))

        return schema_graph
        #self.jira_graph = new_graph
        #self.jira_graph.render_puml()
        #return self.puml()

    def puml(self):
        return self.jira_graph.puml.puml