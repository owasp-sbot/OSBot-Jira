import json
import unittest
from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.api.jira.Jira_Commands import Jira_Commands


@unittest.skip('Need direct access')
class Test_Jira_Commands(TestCase):

    def setUp(self):
        self.api = Jira_Commands()

    def test_projects(self):
        result = self.api.projects()
        Dev.pprint(result)

    def test_issue(self):
        Dev.pprint(self.api.issue(params=['AAA-12' ]))
        Dev.pprint(self.api.issue(params=['RISK-12']))

    def test_update(self):
        event_data = { "Key":"RISK-12" , "Summary": "Dynamically changed ... via unit test" }
        params = json.dumps(event_data).split(' ')
        Dev.pprint(self.api.update(params=params ))