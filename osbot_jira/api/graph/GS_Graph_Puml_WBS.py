class GS_Graph_Puml_WBS:
    edges: list
    nodes: list

    def __init__(self, graph):
        self.graph        = graph
        self.puml_options = graph.puml_options
        self.issues       = graph.issues
        self.nodes        = graph.nodes
        self.edges        = graph.edges
        self.notes        = graph.notes
        self.node_type    = graph.node_type
        self.puml         = graph.puml
        self.skin_params  = graph.skin_params

