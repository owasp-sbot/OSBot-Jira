from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.api.slack.API_Slack_Blocks import API_Slack_Blocks


class test_API_Slack_Blocks(TestCase):
    def setUp(self):
        self.api     = API_Slack_Blocks()
        self.result  = None
        self.channel = 'DDKUZTK6X'
        self.team_id = 'T7F3AUXGV'

    def tearDown(self):
        self.send_message()
        if self.result is not None:
            Dev.pprint(self.result)

    def send_message(self):
        assert self.api.send_message(self.channel, self.team_id).get('ok') is True

    def test_set_text(self):
        self.api.set_text('this is an text using the api that supports blocks')

    def test_add_divider(self):
        self.api.set_text('with divider').add_divider()