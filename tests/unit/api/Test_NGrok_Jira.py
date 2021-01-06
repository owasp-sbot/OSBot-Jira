from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jira.api.NGrok_Jira import NGrok_Jira


class Test_NGrok_Jira(TestCase):

    def setUp(self):
        self.jira = NGrok_Jira()

    def test_invoke(self):
        assert 'v0' in self.jira.invoke('version').get('gsbot_jira')

    def test_issue(self):
        assert self.jira.issue('RISK-12').get('result').get('Key') == 'RISK-12'

    def test_update(self):
        assert self.jira.update('RISK-12','Summary','NGrok test 123') == {'code': 202, 'result': 'update request sent', 'status': 'ok'}

    def test_projects(self):
        Dev.pprint(self.jira.projects())

    def test_version(self):
        assert 'v0' in self.jira.invoke('version').get('gsbot_jira')