from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev
from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_jira.Deploy import Deploy
from osbot_jira.api.slack.views.Jira_Slack_Actions import Jira_Slack_Actions


class test_Jira_Slack_Actions(TestCase):

    def setUp(self):
        self.slack_actions = Jira_Slack_Actions()
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_get_actions_ui(self):
        text,attachments =  self.slack_actions.get_actions_ui()
        slack_message(text, attachments, 'DDKUZTK6X')


    def test_handle_action(self):
        self.result = self.slack_actions.handle_action({'actions': [{'value':'create_issue'}]})


    def test__update_all_lambdas(self):
        Deploy('osbot_jira.lambdas.elastic_jira'      ).deploy()             # update the actions menu
        Deploy('osbot_jira.lambdas.slack_actions'     ).deploy()             # update the callback action
        Deploy('osbot_jira.lambdas.slack_jira_actions').deploy()             # update the jira actions

    def test__update_lambda(self):
        Deploy('osbot_jira.lambdas.slack_actions').deploy()

    def test__invoke_lambda(self):
        self.test__update_lambda()
        payload = {'params': ['actions'], 'channel':'DDKUZTK6X', 'team_id':'T7F3AUXGV'}
        self.result = Lambda('osbot_jira.lambdas.elastic_jira').invoke(payload)

    def test_show_issue(self):
        issue_id = 'SEC-11782'
        payload = {'params': [issue_id], 'channel':'DDKUZTK6X', 'team_id':'T7F3AUXGV'}
        self.result = Lambda('osbot_jira.lambdas.elastic_jira').invoke(payload)