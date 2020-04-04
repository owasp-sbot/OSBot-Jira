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

    def test_render(self):
        print()
        print(self.graph_dot.render())

    def test_render_svg(self):
        result = self.graph_dot.render_svg()
        svg    = result.get('svg')
        if svg:
            file_create(self.svg_file,svg)
        else:
            self.result = result

    def test_sample_dot_graph(self):
        #self.test_graph.add_node('aaa', data={'shape':'box', 'color':'red'})
        #self.graph_dot.set_label('aaaa').set_node_param('shape','box')
        self.result = self.graph_dot.render_svg_to_file(self.svg_file)
        #self.graph_dot.print_dot_code()

    def test_from_graph(self):
        graph = Graph()
        #graph_name = 'graph_QIN'  # (SOW-18 128 nodes)
        #graph_name = 'graph_YXT' # person-42 (manages, 43 nodes)
        #graph_name = 'graph_CXJ'   # Playbook-2 (103 nodes)
        graph_name = 'graph_SCE'  # PERSON-4 (8 nodes)

        graph_dot = Lambda_Graph().get_graph_dot(graph_name)

        (graph_dot.set_layout_engine_dot()
                  .set_rank_dir('LR')
                  .set_rank_same  (['TEAM-2'  , 'TASK-177', 'GUID-4'])
                  .set_rank_source(['TASK-166', 'a b c'])
                  .set_rank_sink  ([ 'GUILD-8'])
                  .render_svg_to_file(self.svg_file))

        print()
        print(graph_dot.render())

    def test_graph__set_rank__set_label__set_node_params(self):
        graph_dot = Lambda_Graph().get_graph_dot('graph_SCE')

        (graph_dot.set_layout_engine_dot()
                  .set_rank_dir('LR')
                  .set_label('This is a title\n\n')
                  .set_node_params({'shape': 'box','color':'deepskyblue', 'style':'filled'})
                  #.set_node_shape('box').set_node_param('fontcolor', 'blue')
                  .set_rank_same  (['TEAM-2'  , 'TASK-177', 'GUID-4'])
                  .set_rank_source(['TASK-166', 'a b c'])
                  .set_rank_sink  ([ 'GUILD-8'])
                  .render_svg_to_file(self.svg_file))
        graph_dot.print_dot_code()