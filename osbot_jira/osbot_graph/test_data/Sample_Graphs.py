from osbot_jira.osbot_graph.Graph import Graph


class Sample_Graphs:

    @staticmethod
    def simple_dot_file():
        graph = Graph()
        graph.add_nodes(['a0','a1', 'a3', 'b2', 'b3','end'])
        graph.add_edges([('a1','b3'), ('b3','end'), ('b2','a3'), ('a3','end'), ('a3','a0')])
        return graph
