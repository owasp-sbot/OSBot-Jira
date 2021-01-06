from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import Files

from osbot_graphsv.demo.Demo_Data_Import import Demo_Data_Import


class test_Demo_Data_Import(TestCase):

    def setUp(self):
        self.demo_data_import = Demo_Data_Import()
        self.result    = None

        self.demo_data_import.indexes.rebuild()

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert Files.folder_exists(self.demo_data_import.demo_data.data_folder) is True

    def test_import_all(self):
        self.demo_data_import.import_all()

    def test_import_Sample_Database_extracts(self):
        self.demo_data_import.import_Sample_Database_extracts__HR_Database()
        self.demo_data_import.import_Sample_Database_extracts__Sunways_application_user_extract()

    def test_dataset__People_Role_Reporting_line(self):
        self.result = self.demo_data_import.import_People_Role_Reporting_line()

    def test_import_Role_Team_Function_Business(self):
        self.result = self.demo_data_import.import_Role_Team_Function_Business()

    def test_import_Device_Person_Account_Application__by_Device(self):
        self.result = self.demo_data_import.import_Device_Person_Account_Application__by_Device()

    def test_import_Device_Person_Account_Application__by_Person(self):
        self.result = self.demo_data_import.import_Device_Person_Account_Application__by_Person()

    def test_import__Device_Person_Account_Application__by_Account(self):
        self.result = self.demo_data_import.import__Device_Person_Account_Application__by_Account()

    def test_import_dataset__Device_Detections(self):
        self.result = self.demo_data_import.import_dataset__Device_Detections()

    def test_import_dataset__Control_Capabilities_Role_People(self):
        self.result = self.demo_data_import.import_dataset__Control_Capabilities_Role_People()

    def test_import_Impacts(self):
        self.result = self.demo_data_import.import_Impacts()

    def test_import_Impact_Vulnerability_Incident_Fact_Control(self):
        self.result = self.demo_data_import.import_Impact_Vulnerability_Incident_Fact_Control()

    def test_import_Incident(self):
        self.result = self.demo_data_import.import_Incident()

    def test_import_Vulnerability_Risk_Role(self):
        self.result = self.demo_data_import.import_Vulnerability_Risk_Role()
