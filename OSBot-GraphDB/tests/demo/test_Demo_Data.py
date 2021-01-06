from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import Files

from osbot_graphsv.demo.Demo_Data import Demo_Data


class test_Demo_Data(TestCase):

    def setUp(self):
        self.demo_data = Demo_Data()
        self.file_name = '1.Sample Database extracts.csv'
        self.result    = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert Files.folder_exists(self.demo_data.data_folder) is True

    # helper methods

    def test_file_lines(self):
        assert len(self.demo_data.file_lines(self.file_name)) == 17

    def test_file_path(self):
        assert Files.exists(self.demo_data.file_path(self.file_name))

    # data sets
    def test_dataset__Sample_Database_extracts__HR_Database(self):
        assert len(self.demo_data.dataset__Sample_Database_extracts__HR_Database()) == 6

    def test_dataset__Sample_Database_extracts__Sunways_application_user_extract(self):
        assert len(self.demo_data.dataset__Sample_Database_extracts__Sunways_application_user_extract()) == 6

    def test_dataset__People_Role_Reporting_line(self):
        assert len(self.demo_data.dataset__People_Role_Reporting_line()) == 6

    def test_dataset__Role_Team_Function_Business(self):
        assert len(self.demo_data.dataset__Role_Team_Function_Business()) == 6

    def test_dataset__Device_Person_Account_Application__by_Device(self):
        assert len(self.demo_data.dataset__Device_Person_Account_Application__by_Device()) == 6

    def test_dataset__Device_Person_Account_Application__by_Person(self):
        assert len(self.demo_data.dataset__Device_Person_Account_Application__by_Person()) == 6

    def test_dataset__Device_Person_Account_Application__by_Account(self):
        assert len(self.demo_data.dataset__Device_Person_Account_Application__by_Account()) == 6

    def test_dataset__Business_Asset(self):
        assert len(self.demo_data.dataset__Business_Asset()) == 6

    def test_dataset__Device_Detections(self):
        assert len(self.demo_data.dataset__Device_Detections()) == 19

    def test_dataset__Account_Detections_2FA(self):
        assert len(self.demo_data.dataset__Account_Detections_2FA()) == 24

    def test_dataset__Control_Capabilities_Role_People(self):
        assert len(self.demo_data.dataset__Control_Capabilities_Role_People()) == 24

    def test_dataset__Impacts(self):
        assert len(self.demo_data.dataset__Impacts()) == 72

    def test_dataset__Impact_Vulnerability_Incident_Fact_Control(self):
        assert len(self.demo_data.dataset__Impact_Vulnerability_Incident_Fact_Control()) == 24

    def test_dataset__Incident(self):
        assert len(self.demo_data.dataset__Incident()) == 40

    def test_dataset__Vulnerability_Risk_Role(self):
        assert len(self.demo_data.dataset__Vulnerability_Risk_Role()) == 11

        # print('-----')
        # for item in self.demo_data.dataset__Account_Detections_2FA():
        #     print(item.get('edge_2'))
