from unittest import TestCase

from dotenv import load_dotenv

from osbot_jira.api.slack.API_Slack import API_Slack
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import env_vars


class test_API_Slack(TestCase):

    def setUp(self) -> None:
        load_dotenv()
        env               = env_vars()
        self.bot_user     = env.get('SLACK_BOT_USER'      )
        self.bot_team_id  = env.get('SLACK_BOT_TEAM_ID'   )
        self.bot_user_id  = env.get('SLACK_BOT_USER_ID'   )
        self.bot_bot_id   = env.get('SLACK_BOT_ID'        )
        self.bot_token    = env.get('SLACK_BOT_USER_TOKEN')
        self.test_channel = env.get('SLACK_TEST_CHANNEL')
        self.api_slack = API_Slack(bot_token=self.bot_token)

    def test__init__(self):
        assert self.api_slack.bot_token == self.bot_token
        auth_test = self.api_slack.slack.auth_test()
        bot_user    = auth_test.get('user')
        bot_team_id = auth_test.get('team_id')
        bot_user_id = auth_test.get('user_id')
        bot_bot_id = auth_test.get('bot_id')
        assert bot_user    == self.bot_user
        assert bot_team_id == self.bot_team_id
        assert bot_user_id == self.bot_user_id
        assert bot_bot_id  == self.bot_bot_id

    # def test_get_channel(self):
    #     result = self.api_slack.get_channel(self.test_channel)
    #     pprint(result)

    def test_send_message(self):
        result = self.api_slack.send_message('hello', channel=self.test_channel)