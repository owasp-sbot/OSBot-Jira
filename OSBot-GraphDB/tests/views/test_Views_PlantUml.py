from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_graphsv.demo.Demo_Data import Demo_Data
from osbot_graphsv.views.GS_Graph_SV import GS_Graph_SV
from osbot_graphsv.views.Views_PlantUml import Views_PlantUml
from osbot_jira.api.graph.GS_Graph import GS_Graph


class test_Views_PlantUml(TestCase):
    def setUp(self):
        self.demo_data      = Demo_Data()
        self.issues         = self.demo_data.graph_sv.issues
        self.links          = self.demo_data.graph_sv.links
        self.views_plantuml = Views_PlantUml()
        self.result = None

        self.demo_data.graph_sv.indexes.rebuild()


    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)


    def test_graph_links(self):

        graph = GS_Graph_SV(self.demo_data.graph_sv)

        for link in self.links.all():
            (from_key,link_type, to_key) = link
            graph.add_node(from_key)
            graph.add_node(to_key)
            graph.add_edge(from_key,link_type,to_key)

        graph.render_puml()
        #self.result = graph.puml.puml
        graph.render_puml_and_save_tmp()

    def test_graph_expand(self):
        issue_id    = 'Person-2'
        link_types  = ['has role','is manager of']
        issue_id = 'Role-2'
        link_types = [ 'reports to','is role of']

        issue_id = 'Business_Unit-1'
        link_types = ['has function', 'funds','is role of']

        depth       = 5

        graph = GS_Graph_SV(self.demo_data.graph_sv)
        graph.set_puml_link_types_to_add(link_types)
        graph.add_all_linked_issues([issue_id],depth)
        graph.render_puml_and_save_tmp()


