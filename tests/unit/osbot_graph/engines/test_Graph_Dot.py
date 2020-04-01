from gw_bot.helpers.Test_Helper                     import Test_Helper
from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph
from osbot_jira.osbot_graph.Graph import Graph
from osbot_jira.osbot_graph.engines.Graph_Dot       import Graph_Dot
from osbot_jira.osbot_graph.test_data.Sample_Graphs import Sample_Graphs
from osbot_utils.utils.Files                        import file_create


class test_Graph_Dot(Test_Helper):

    def setUp(self):
        super().setUp()
        self.svg_file   = '/tmp/dot_image.svg'
        self.test_graph = Sample_Graphs.simple_dot_file()
        self.graph_dot  = Graph_Dot(self.test_graph)

    def test_dot(self):
        print()
        print(self.graph_dot.dot())

    def test_render_svg(self):
        result = self.graph_dot.render_svg()
        svg    = result.get('svg')
        if svg:
            file_create(self.svg_file,svg)
        else:
            self.result = result

    def test_from_graph(self):
        graph = Graph()
        #graph_name = 'graph_QIN'  # large
        graph_name = 'graph_YXT'
        graph_name = 'graph_SCE'
        graph_data = Lambda_Graph().get_graph_data(graph_name)
        nodes = graph_data.get('nodes').keys()
        edges = graph_data.get('edges')
        graph.add_nodes(nodes)
        graph.add_edges(edges)

        graph_dot = Graph_Dot(graph)

        (graph_dot.set_layout_engine_dot()
                  .set_rank_dir('LR')
                  .set_rank_same  (['TEAM-2'  , 'TASK-177', 'GUID-4'])
                  .set_rank_source(['TASK-166', 'a b c'])
                  .set_rank_sink  ([ 'GUILD-8'])
                  .render_svg_to_file(self.svg_file))

        print()
        print(graph_dot.dot())
