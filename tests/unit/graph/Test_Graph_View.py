from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jira.api.graph.Graph_View import Graph_View


class Test_Graph_View(TestCase):
    def setUp(self):
        self.graph_views = Graph_View()

    def test_handle_lambda_request(self):
        graph = self.graph_views.handle_lambda_request(['sec-9696-down', 'by_status'],'DDKUZTK6X')
        graph.puml.save_tmp()

    def test_bad_params_message(self):
        result = self.graph_views.bad_params_message()

        Dev.pprint(result)

    def test_load_graph(self):
        self.graph_views.load_graph('sec-9696-down')
        Dev.pprint(len(self.graph_views.graph.nodes))
        self.graph_views.load_graph('sec-9696-up')
        Dev.pprint(len(self.graph_views.graph.nodes))


    def test_render_by_labels(self):
        name = 'graph_SUG'
        #self.graph_views.load_graph(name).render_by_labels()               # old version of doing this
        self.graph_views.load_graph(name).render_view('by_labels',  'DDKUZTK6X', 'T7F3AUXGV', name)
        self.graph_views.graph.puml.save_tmp()

    def test_render_top_down(self):
        name = 'graph_SUG'
        self.graph_views.load_graph(name)           \
                         .view_top_down()           \
                         .graph.puml.save_tmp()


    def test_render_top_down__via_render_view(self):
        name = 'graph_8M3'
        self.graph_views.load_graph(name).render_view('top_down', None)
        self.graph_views.graph.puml.save_tmp()



    def test_render_link_types(self):
        (
            self.graph_views
                    .load_graph('graph_8M3')
                    .render_view('links', None)
                    .print_puml()
                    .graph.puml.save_tmp()
        )

    def test_render_view__dynamic_name(self):
        self.graph_views.load_graph('graph_2ZA')

        graph = self.graph_views.graph

        assert graph.puml.puml == '@startuml\n'
        assert ("@enduml" in graph.puml.puml) is False

        self.graph_views.render_view('default', 'DDKUZTK6X')

        #assert ("@enduml" in graph.puml.puml) is True


    def test_view_schema(self):
        #graph_name = 'graph_MRK'
        graph_name = 'graph_R06'  #
        #graph_name = 'graph_H2Q'  # really big one
        #graph_name = 'graph_9HT'
        (self.graph_views.load_graph(graph_name)
                         .view_schema()
                         .graph.puml.save_tmp())

    def test_view_with_colors(self):
        graph_name = 'graph_MRK'
        #graph_name = 'graph_BLO'
        graph_name ='graph_7ZB'
        (self.graph_views.load_graph(graph_name)
                         .view_colors()
                         .graph.puml.save_tmp())

        Dev.print(self.graph_views.graph.puml.puml)

