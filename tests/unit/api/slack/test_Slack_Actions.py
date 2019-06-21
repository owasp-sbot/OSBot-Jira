from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.slack.API_Slack_Dialog import API_Slack_Dialog

from osbot_jira.Deploy import Deploy
from osbot_jira.api.slack.Slack_Actions import Slack_Actions
from osbot_jira.api.slack.Slack_Jira_Search import Slack_Jira_Search


class test_Slack_Actions(TestCase):
    def setUp(self):
        self.slack_actions = Slack_Actions()
        self.result        = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)


    def test_handle_interactive_message(self):
        target = self.slack_actions.handle_interactive_message
        assert target({'callback_id': 'abc'}) == { 'attachments': [],'replace_original': False,'text': ':red_circle: requested action currently not supported: `abc`'}

        self.result = target({'callback_id': 'jira-slack-actions'})

    def test_handle_dialogue_suggestions(self):
        self.test__update_lambda_slack_actions()
        channel            = 'DDKUZTK6X'
        (text,attachments) = Slack_Jira_Search().get_drop_box_ui()
        slack_message(text, attachments, channel)


    def test__update_lambda_slack_actions(self):
        Deploy('osbot_jira.lambdas.slack_actions').deploy()
