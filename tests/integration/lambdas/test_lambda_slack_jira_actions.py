import unittest
from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment

class test_lambda_gsbot_gs_jira(TestCase):

    def setUp(self):
        self.lambda_name = 'osbot_jira.lambdas.slack_jira_actions'
        self.aws_lambda = Lambda(self.lambda_name)
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test___bad_action(self):
        self.test_lambda_update()
        payload = {  #'channel': 'GDL2EC3EE'
                     # 'team_id':'T7F3AUXGV'
                       "data": { "callback_id": 'abc',
                                 "submission" : {

                    }}}
        self.result = payload
        self.result = self.aws_lambda.invoke(payload)


    def test_lambda_update(self):
        Lambda_Package(self.lambda_name).update_code()

    def test_lambda_invoke(self):
        self.test_lambda_update()
        self.result = self.aws_lambda.invoke()
