from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.Deploy import Deploy
from osbot_jira.api.slack.Slack_Jira_Search import Slack_Jira_Search


class test_Slack_Jira_Search(TestCase):
    def setUp(self):
        self.result = None
        self.slack_jira_search = Slack_Jira_Search()

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_from_select_box(self):
        data = {'channel' : {'id': None}, 'team' : {'id': None}, 'value': 'test'}
        self.result = self.slack_jira_search.from_select_box(data)

    def test__update_lambda_slack_actions(self):
        Deploy('osbot_jira.lambdas.slack_actions').deploy()