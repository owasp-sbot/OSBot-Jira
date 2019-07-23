import pydot

from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
from pbx_gs_python_utils.utils.Show_Img import Show_Img


class API_Pydot:
    def __init__(self, slack_channel = None ):
        self.graph         = pydot.Dot(graph_type='digraph')
        self.slack_channel = slack_channel

    def add_node(self, text, shape     = None, color    = None, comment  = None, fillcolor = None,
                             fontcolor = None, fontname = None, fontsize = None, height    = None,
                             image     = None, label    = None, margin   = None, width     = None,
                             style     = None   ):
        node = pydot.Node(text)
        self.graph.add_node(node)
        if shape     : node.set_shape    (shape)
        if color     : node.set_color    (color)
        if comment   : node.set_comment  (comment)
        if fillcolor : node.set_fillcolor(fillcolor)
        if fontcolor : node.set_fontcolor(fontcolor)
        if fontname  : node.set_fontname (fontname)
        if fontsize  : node.set_fontsize (fontsize)
        if height    : node.set_height   (height)
        #if image     : node.set_image    (image)           # todo: figure out how this works
        if label     : node.set_label    (label)
        if margin    : node.set_margin   (margin)
        if style     : node.set_style(style)
        if width     : node.set_width    (width)

        return node

    def add_edge(self, from_node, to_node):
        if type(from_node) is str:
            from_node = pydot.Node(from_node)
        if type(to_node) is str:
            to_node = pydot.Node(to_node)
        edge = pydot.Edge(from_node,to_node)
        self.graph.add_edge(edge)
        return edge


    def dot(self):
        return self.graph.to_string()

    def dpi(self, value):       # not working for lambda generated files
        self.graph.set_dpi(value)
        return self

    def save(self,path=None):
        if path is None:
            path = '/tmp/api-pydot-test.png'
        self.graph.write_png(path, prog='dot')
        return path

    def show(self):
        Show_Img.from_path(self.save())

    def send_to_slack(self):
        #dot = self.dot().replace('digraph G {\n', 'digraph G {\n graph [height="500"];\n' )
        dot = self.dot()
        API_Slack(self.slack_channel).dot_to_slack(dot)



    # def pydot(self):
    #     data = Files.contents('../data/TM_Graph.dot')
    #
    #
    #     d = 'digraph {\na -> b[label="hi", decorate];\n}'
    #     graph = pydot.graph_from_dot_data(data).pop()
    #
    #     node = pydot.Node('test_1234', shape="box")
    #     graph.add_node(node)
    #     jpe_data = graph.create(format='jpe', encoding='ascii')
    #
    #     filename = 'test_dot'
    #     graph.write_png(filename + '.png', prog='dot')
    #     return graph.write_dot(filename + '.dot', prog='dot')
    #     #return jpe_data

