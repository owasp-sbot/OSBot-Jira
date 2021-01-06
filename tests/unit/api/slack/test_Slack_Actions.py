from osbot_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_jira.api.slack.Slack_Actions import Slack_Actions
from osbot_jira.api.slack.Slack_Jira_Search import Slack_Jira_Search
from osbot_jira.lambdas.slack_actions import run


class test_Slack_Actions(Test_Helper):

    def setUp(self):
        super().setUp()
        self.slack_actions = Slack_Actions()

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_update_lambda(self):
        Deploy().deploy_lambda__jira('osbot_jira.lambdas.slack_actions')

    def test_invoke_directly(self):
        self.result = run({'data':'eld ata'})

    def test_handle_interactive_message(self):
        target = self.slack_actions.handle_interactive_message
        assert target({'callback_id': 'abc'}) == { 'attachments': [],'replace_original': False,'text': ':red_circle: Requested action currently not supported: `abc`'}

        self.result = target({'callback_id': 'jira-slack-actions'})

    def test_handle_dialogue_suggestions(self):
        #self.test__update_lambda_slack_actions()
        channel            = 'DDKUZTK6X'
        (text,attachments) = Slack_Jira_Search().get_drop_box_ui()
        slack_message(text, attachments, channel)





    def test_handle_block_action_(self):
        event = {'actions': [{'action_id': 'class_method::Jira_View_Issue::issue_links'}],
                 'team': {'id': 'asd'}}
        self.result = self.slack_actions.handle_block_action(event)

