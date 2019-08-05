from osbot_graphsv.views.GS_Graph_SV import GS_Graph_SV

class Views_PlantUml:

    def __init__(self, graph_sv):
        self.graph_sv = graph_sv
        self.links    = self.graph_sv.links

    def graph_all_nodes(self):
        graph = GS_Graph_SV(self.graph_sv)

        for link in self.links.all():
            (from_key,link_type, to_key) = link
            graph.add_node(from_key)
            graph.add_node(to_key)
            graph.add_edge(from_key,link_type,to_key)
        graph.render_puml()
        return graph

    def graph_expand(self, issue_id, depth, link_types):
        graph = GS_Graph_SV(self.graph_sv)
        graph.set_puml_link_types_to_add(link_types)
        graph.add_all_linked_issues([issue_id], depth)
        return graph

    def graph_schema_from_graph(self, graph):

        issues = graph.get_nodes_issues()
        schema = {}
        puml = graph.puml
        for edge in graph.edges:
            if issues[edge[0]]:
                from_issue_type = puml.fix_id(issues[edge[0]].get('Issue Type'))
            else:
                from_issue_type = 'NA'
            link_name = edge[1]
            if issues[edge[2]]:
                to_issue_type = puml.fix_id(issues[edge[2]].get('Issue Type'))
            else:
                to_issue_type = 'NA'
            schema_edge = (from_issue_type, link_name, to_issue_type)
            if schema.get(schema_edge) is None: schema[schema_edge] = {'count': 0,
                                                                       'from_issue_type': from_issue_type,
                                                                       'link_name': link_name,
                                                                       'to_issue_type': to_issue_type}
            schema.get(schema_edge)['count'] += 1

        new_graph = GS_Graph_SV(self.graph_sv)
        for item in schema.values():
            new_graph.add_node(item.get('from_issue_type'))
            new_graph.add_node(item.get('to_issue_type'))
            new_graph.add_edge(item.get('from_issue_type'), item.get('link_name'), item.get('to_issue_type'))

        return new_graph

        def graph_with_schema(self):
            graph_with_all_nodes = self.graph_all_nodes()
            graph_with_schema    = self.views_plantuml.graph_schema_from_graph(graph_with_all_nodes)
            return graph_with_schema
