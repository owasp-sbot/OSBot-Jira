from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_graphsv.api.Issues import Issues
from osbot_graphsv.demo.Demo_Data import Demo_Data


class test_Issues(TestCase):

    def setUp(self):
        self.demo_data = Demo_Data()
        self.issues = Issues(self.demo_data.file_system())
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    # def test_all(self):
    #     assert len(self.issues.all()) > 15