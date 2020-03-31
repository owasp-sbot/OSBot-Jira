from osbot_aws.apis.Lambda import Lambda


class Graph_Dot:

    def __init__(self,graph):
        self.graph = graph

    def dot(self):
        digraph = "digraph G { \n"
        digraph += '\t\t\t####### Nodes #######\n'
        for node in self.graph.nodes():
            key = node.get('key')
            digraph += f'\t\t\t"{key}"\n'

        digraph += '\t\t\t####### Edges #######\n'
        for edge in self.graph.edges():
            from_key = edge.get('from')
            to_key   = edge.get('to')
            digraph += f'\t\t\t"{from_key}" -> "{to_key}"\n'
        digraph +='          }'
        return digraph

    def render_svg(self):
        return Lambda('gw_bot.lambdas.dot_to_png').invoke({'dot':self.dot()})

