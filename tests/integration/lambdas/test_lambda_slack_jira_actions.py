from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from osbot_utils.utils.Dev import Dev

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
        payload = {
                       "data": { "callback_id": 'abc',
                                 "submission" : { 'callback_id' : 'abc' }}}
        assert self.aws_lambda.invoke(payload) == ':red_circle: Sorry, action not recognized : abc'

    def test___action_show_issue_screenshot(self):
        self.test_lambda_update()
        payload = {  'channel': 'DDKUZTK6X' ,
                     'team_id':'T7F3AUXGV'  ,
                     "data": { "callback_id": 'show_issue_screnshot',
                                 "submission" : { 'callback_id' : 'show_issue_screnshot' , 'issue_id':'RISK-12'}}}
        self.result = self.aws_lambda.invoke(payload)

    def test___action_jira_create_issue(self):
        self.test_lambda_update()
        payload = {  'channel': 'DDKUZTK6X' ,
                     'team_id':'T7F3AUXGV'  ,
                     "data"   : {   "callback_id": 'jira_create_issue',
                                    "submission" : { 'callback_id' : 'show_issue_screnshot' ,
                                                     'project'      : 'SEC',
                                                     'issue_type'   : 'Task',
                                                     'summary'      : 'an test issue',
                                                     'description'  : 'an test description'}}}
        self.result = self.aws_lambda.invoke(payload)



    def test_lambda_update(self):
        Lambda_Package(self.lambda_name).update_code()

    def test_lambda_invoke(self):
        self.test_lambda_update()
        self.result = self.aws_lambda.invoke()
