from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.api.slack.Slack_Actions import Slack_Actions


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