from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from osbot_graphsv.demo.Demo_Data_Import import Demo_Data_Import


class test_Demo_Data_Import(TestCase):

    def setUp(self):
        self.demo_data_import = Demo_Data_Import()
        self.result    = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert Files.folder_exists(self.demo_data_import.demo_data.data_folder) is True

    def test_import_Sample_Database_extracts__HR_Database(self):
        self.result = self.demo_data_import.import_Sample_Database_extracts__HR_Database()