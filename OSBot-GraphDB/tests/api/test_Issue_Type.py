from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_graphsv.api.Graph_SV import Graph_SV
from osbot_graphsv.demo.Demo_Data import Demo_Data


class test_Issue_Type(TestCase):
    def setUp(self):
        self.demo_data   = Demo_Data()
        self.graph_sv    = Graph_SV(self.demo_data.root_folder)
        self.file_system = self.graph_sv.file_system
        self.result      = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_issue_type_path(self):
        assert 'GraphSV-demo-data/data/AAAA'     in self.file_system.issue_type('AAAA'    ).path()
        assert 'GraphSV-demo-data/data/AAAA.aaa' in self.file_system.issue_type('AAAA.aaa').path()
        self.file_system.issue_type('AAAA'    ).delete()
        self.file_system.issue_type('AAAA.aaa').delete()

    def test_issue_add(self):
        name = 'To Add Tests'
        data = { 'the_answer': 'is 42'}
        issue_type = self.file_system.issue_type(name)
        issue_type.create()

        result = issue_type.issue_add(data)
        assert result.get('status') == 'ok'
        issue_key = result.get('issue_key')
        assert issue_type.issue_get(issue_key) == {'Issue Type': 'To Add Tests', 'Key': 'To_Add_Tests-1', 'the_answer': 'is 42'}

        issue_type.delete()

    def create(self):
        name = 'AAAA BB CC'
        issue_type = self.file_system.issue_type(name)
        #issue_type.delete()
        assert issue_type.exists() is False
        assert issue_type.create() == {'data': 'issue type created: ' + name, 'status': 'ok'}
        assert issue_type.create() == {'data': 'issue type already existed: ' + name, 'status': 'error'}
        assert issue_type.exists() is True
        assert issue_type.metadata() == {'Issue Type': 'AAAA BB CC', 'Key Id': 'AAAA_BB_CC', 'Next Key': 1}
        assert issue_type.delete() == True
