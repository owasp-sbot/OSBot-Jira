import json
from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jira.api.jira_server.Jira_Commands import Jira_Commands


class Test_Jira_Commands(TestCase):

    def setUp(self):
        self.api = Jira_Commands()

    def test_projects(self):
        result = self.api.projects()
        Dev.pprint(result)

    def test_issue(self):
        assert 'project `AAA` is currently not available' in self.api.issue(params=['AAA-12' ]).get('error')
        assert self.api.issue(params=['RISK-12']).get('Key') =='RISK-12'

    def test_update(self):
        event_data = { "Key":"RISK-12" , "Summary": "Dynamically changed ... via unit test ..." }
        params = json.dumps(event_data).split(' ')
        assert self.api.update(params=params ) == {'status': 'ok'}