from gw_bot.helpers.Test_Helper                     import Test_Helper
from osbot_jira.osbot_graph.engines.Graph_Dot       import Graph_Dot
from osbot_jira.osbot_graph.test_data.Sample_Graphs import Sample_Graphs
from osbot_utils.utils.Files                        import file_create


class test_Graph_Dot(Test_Helper):

    def setUp(self):
        super().setUp()
        self.test_graph = Sample_Graphs.simple_dot_file()
        self.graph_dot = Graph_Dot(self.test_graph)

    def test_dot(self):
        print()
        print(self.graph_dot.dot())

    def test_render_svg(self):
        result = self.graph_dot.render_svg()
        svg    = result.get('svg')
        if svg:
            file_create('/tmp/aaa.svg',svg)
        else:
            self.result = result