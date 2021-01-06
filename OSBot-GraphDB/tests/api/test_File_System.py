from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import Files

from osbot_graphsv.api.Graph_SV import Graph_SV
from osbot_graphsv.demo.Demo_Data import Demo_Data


class test_File_System(TestCase):

    def setUp(self):
        self.demo_data   = Demo_Data()
        self.graph_sv    = Graph_SV(self.demo_data.root_folder)
        self.file_system = self.graph_sv.file_system
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert Files.folder_exists(self.file_system.folder_root)
        assert Files.folder_exists(self.file_system.folder_data)
        assert Files.folder_exists(self.file_system.folder_indexes)

    def test_safe_string(self):
        assert self.file_system.safe_string("AbZ_-!@£$%\".123") == 'AbZ_-_.123'
        assert self.file_system.safe_string("AbZ_-. 123      ") == 'AbZ_-._123'
        assert self.file_system.safe_string("AA BB CC        ") == 'AA_BB_CC'

