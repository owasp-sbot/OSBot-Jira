from osbot_aws.apis.Lambda import Lambda
from gw_bot.helpers.Test_Helper import Test_Helper

from gw_bot.Deploy import Deploy
from osbot_jira.lambdas.gw.gw_jira import run


class test_sow(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_jira.lambdas.gw.gw_jira'
        self.aws_lambda  = Lambda(self.lambda_name)
        self.result      = None
        self.png_data    = None

    def tearDown(self):
        super().print(self.result)
        super().save_png(self.png_data, '/tmp/lambda_png_file.png')

    #def test_update_lambda(self):
    #    Deploy().setup().deploy_lambda__browser(self.lambda_name)

    def test_invoke_directly(self):
        payload = {}
        self.result = run(payload, None)