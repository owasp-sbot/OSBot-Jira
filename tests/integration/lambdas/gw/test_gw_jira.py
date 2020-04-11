from gw_bot.Deploy                  import Deploy
from gw_bot.helpers.Test_Helper     import Test_Helper
from osbot_aws.apis.Lambda          import Lambda
from osbot_jira.lambdas.gw.gw_jira  import run


class test_sow(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_jira.lambdas.gw.gw_jira'
        self.aws_lambda  = Lambda(self.lambda_name)
        self.result      = None

    def tearDown(self):
        super().print(self.result)

    def test_update_lambda(self):
        Deploy().setup().deploy_lambda__jira(self.lambda_name)

    def test_invoke_directly(self):
        payload = { "issue_id": "PERSON-1"}
        self.result = run(payload, None)


    def test_invoke_in_lambda(self):
        self.test_update_lambda()
        payload = {"issue_id": "SOW-121"}
        self.result = self.aws_lambda.invoke(payload)



#    for this to work run this command on the tests folder
#         pip3 install -t _lambda_dependencies/jira jira
#    def test_update_dependency(self):
#         upload_dependency('jira')
