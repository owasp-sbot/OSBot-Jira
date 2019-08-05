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