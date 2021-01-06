from unittest import TestCase

from gw_bot.Deploy import Deploy
from osbot_utils.utils.Dev import Dev

from osbot_jira.api.slack.Slack_Message_Action import Slack_Message_Action


class test_Slack_Message_Action(TestCase):

    def setUp(self):
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_jira_create_issue_from_slack_message(self):

        message = {'client_msg_id': 'b4b37af8-6137-4702-be0f-4617493d4443', 'type': 'message', 'text': 'this+is+a+test+message', 'user': 'U7ESE1XS7', 'ts': '1561014418.000500', 'edited': {'user': 'U7ESE1XS7', 'ts': '1561016096.000000'}}
        action_ts = '1561016153.942837'
        self.result = Slack_Message_Action(message, action_ts).jira_create_issue_from_slack_message()


    def test__update_lambda(self):
        Deploy('osbot_jira.lambdas.slack_actions').deploy()
