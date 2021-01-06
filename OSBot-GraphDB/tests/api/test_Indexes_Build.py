from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import Files
from osbot_graphsv.api.Indexes_Build import Indexes_Build
from osbot_graphsv.demo.Demo_Data import Demo_Data


class test_Indexes_Build(TestCase):

    def setUp(self):
        self.file_system   = Demo_Data().file_system()
        #self.issues        = Issues(self.file_system)
        self.indexes_build = Indexes_Build(self.file_system)
        self.result = None


    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert Files.exists(self.indexes_build.file_system.folder_root)

    def test_create_all(self):
        self.indexes_build.create_all()

    def test_create__by_key(self):
        self.result = self.indexes_build.create__by_key()

    def test_create__by_link_type(self):
        self.indexes_build.create__by_link_type()
        self.result = self.indexes_build.get__by_link_type()

        # def test_create__by_fields_and_values(self):
    #     self.name = 'AAA BBB'
    #     self.issue_type = Issue_Type(self.file_system, self.name).setup()
    #
    #     self.issue_type.issue_add({'Summary': 'abc'})
    #     self.issue_type.issue_add({'Summary': Misc.random_string_and_numbers()})
    #     self.issue_type.issue_add({'Summary': Misc.random_string_and_numbers()})
    #     self.issue_type.issue_add({'Summary': Misc.random_string_and_numbers()})
    #     self.issue_type.issue_add({'Summary': 'abc'})
    #
    #
    #     self.indexes_build.create__by_key()
    #
    #     assert self.indexes_build.create__by_fields_and_values().get('Summary').get('abc') == ['AAA_BBB-1', 'AAA_BBB-5']
    #     assert self.indexes_build.get__by_fields_and_values()   .get('Summary').get('abc') == ['AAA_BBB-1', 'AAA_BBB-5']
    #
    #     self.issue_type.delete()

    # def test_create__by_values(self):
    #     self.result = self.indexes_build.create__by_values()

