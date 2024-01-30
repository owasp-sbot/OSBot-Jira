from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_aws.helpers.Test_Helper import Test_Helper

from osbot_jira.api.slack.Slack_Jira_Search import Slack_Jira_Search


class test_Slack_Jira_Search(Test_Helper):
    def setUp(self):
        super().setUp()
        self.slack_jira_search = Slack_Jira_Search()

    def test__update_lambda_slack_actions(self):
        Deploy().deploy_lambda__jira('osbot_jira.lambdas.slack_actions')

    def test_from_select_box(self):
#        self.test__update_lambda_slack_actions()
        data = {'channel' : {'id': None}, 'team' : {'id': None}, 'value': 'test'}
        self.result = self.slack_jira_search.from_select_box(data)

    def test_return_search_results(self):
        self.result = self.slack_jira_search.return_search_results('people dinis')

    def test_get_drop_box_ui(self):
        channel = 'DRE51D4EM'
        (text, attachments) = Slack_Jira_Search().get_drop_box_ui()
        slack_message(text, attachments, channel)

