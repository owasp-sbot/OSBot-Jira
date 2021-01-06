from    osbot_aws.apis.Lambda import Lambda

from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_jira.lambdas.elk_to_slack import run


class test_elk_to_slack(Test_Helper):
    def setUp(self):
        super().setUp()
        self.jira_issues = Lambda('osbot_jira.lambdas.elk_to_slack')

    def test_update_lambda(self):
        Deploy().deploy_lambda__jira('osbot_jira.lambdas.elk_to_slack')

    def test_invoke_directly(self):
        response = run({},{})
        self.result = response

    def test_invoke_directly__people(self):
        self.result = run({'params':['search','people','Dinis']},{})



    def test_invoke_lambda(self):
        self.test_update_lambda()
        self.result = self.jira_issues.invoke({"params": ['search','people','Dinis']})