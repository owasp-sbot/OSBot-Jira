from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_graphsv.api.Graph_SV import Graph_SV
from osbot_graphsv.demo.Demo_Data import Demo_Data


class test_Graph_SV(TestCase):

    def setUp(self):
        self.demo_data   = Demo_Data()
        self.graph_sv = Graph_SV(self.demo_data.root_folder)
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert type(self.graph_sv.file_system).__name__ == 'File_System'
