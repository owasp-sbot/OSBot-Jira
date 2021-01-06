from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jira.Jira import Jira


class test_Jira(TestCase):

    def setUp(self):
        self.jira  = Jira()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__helper_classes(self):
        assert self.jira.elk_to_slack()  .__module__ == 'osbot_jira.api.elk.Elk_To_Slack'
        assert self.jira.graph_commands().__module__ == 'osbot_jira.api.graph.Lambda_Graph_Commands'
        assert self.jira.gs_bot_jira()   .__module__ == 'osbot_jira.api.GS_Bot_Jira'
        assert self.jira.api_issues()    .__module__ == 'osbot_jira.api.API_Issues'

    def test_api_issues(self):
        assert self.jira.api_issues().index           == 'jira,it_assets,sec_project'
        assert self.jira.api_issues().elastic().index == 'jira,it_assets,sec_project'


    def test_elk_to_slack(self):
        self.result = self.jira.elk_to_slack()


    def test_issue(self):
        assert self.jira.issue('Risk-12').get('Key') == 'RISK-12'

    def test_issues(self):
        assert len(self.jira.issues(['RISK-12','RISK-42'])) == 2

    def test_search(self):
        self.result = self.jira.search('"RISK-12"')

    def test_graph_links(self):
        self.result = self.jira.graph_links('GSSP-111', 'up',1).to_json()









