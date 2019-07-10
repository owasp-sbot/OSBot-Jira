from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

from osbot_jira.Deploy import Deploy
from osbot_jira.api.slack.views.Jira_View_Issue import Jira_View_Issue


class test_Jira_View_Issue(TestCase):
    def setUp(self):
        self.jira_view_issue          = Jira_View_Issue()
        self.lambda_name_jira_actions = 'osbot_jira.lambdas.slack_actions'
        self.result                   = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__update_lambda_slack_actions(self):
        Deploy(self.lambda_name_jira_actions).deploy()            # update the lambda that handles the callbacks


    def test_create_and_send(self):
        self.test__update_lambda_slack_actions()
        self.jira_view_issue.issue_id = 'FACT-42' #RISK-1524' #''SEC-11961'
        self.jira_view_issue.channel  = 'DDKUZTK6X'
        self.jira_view_issue.team_id  = 'T7F3AUXGV'
        self.result = self.jira_view_issue.create_and_send()

    # def test_invoke_via_lambda__edit_issue(self):
    #     self.test__update_lambda_slack_actions()
    #     payload = {
    #                     'type'       : 'interactive_message',
    #                     'actions'    : [{'name': 'jira-view-issue', 'type': 'button', 'value': 'edit_issue'}],
    #                     'callback_id': 'jira-view-issue',
    #                     'team'       : {'id': 'T7F3AUXGV', 'domain': 'gs-cst'},
    #                     'channel'    : {'id': 'DDKUZTK6X', 'name': 'directmessage'},
    #                     'user'       : {'id': 'U7ESE1XS7', 'name': 'dinis.cruz'},
    #               }
    #     self.result = Lambda(self.lambda_name_jira_actions).invoke(payload)
    #     print('here')
    #
    # def test_get_actions_ui(self):
    #     self.test__update_lambda_slack_actions()
    #     issue_id = 'SEC-11961'
    #     text, attachments = Jira_View_Issue(issue_id).get_actions_ui()
    #
    #     slack_message(text,attachments, 'DDKUZTK6X','T7F3AUXGV')
    #
    #
    #     self.result = attachments
