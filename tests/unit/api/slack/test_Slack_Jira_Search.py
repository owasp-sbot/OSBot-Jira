from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from gw_bot.helpers.Lambda_Helpers import slack_message

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
        self.test__update_lambda_slack_actions()
        data = {'channel' : {'id': None}, 'team' : {'id': None}, 'value': 'test'}
        self.result = self.slack_jira_search.from_select_box(data)

    def test_return_search_results(self):
        self.result = self.slack_jira_search.return_search_results('people dinis')

    def test_get_drop_box_ui(self):
        channel = 'DDKUZTK6X'
        (text, attachments) = Slack_Jira_Search().get_drop_box_ui()
        slack_message(text, attachments, channel)

    def test__update_lambda_slack_actions(self):
        Deploy('osbot_jira.lambdas.slack_actions').deploy()