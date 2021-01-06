from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package

from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_utils.utils.Dev import Dev

from osbot_jira.lambdas.graph import run


class test_lambda_gsbot_graph(Test_Helper):
    def setUp(self):
        super().setUp()
        self.lambda_graph = Lambda_Package('osbot_jira.lambdas.graph')
        self.result       = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)


    def test_invoke_directly(self):
        response = run({},{})
        Dev.pprint(response)

    def test_invoke_directly_raw_data(self):
        graph_name = 'graph_J2O'
        payload = {'params': ['raw_data', graph_name, 'details'], 'data': {}}
        # data = Lambda('lambdas.gsbot.gsbot_graph').invoke(params)
        self.result = run(payload,{})
        #self.results = Lambda('osbot_jira.lambdas.graph').invoke(params)

    def test_update_lambda(self):
        Deploy().deploy_lambda__jira('osbot_jira.lambdas.graph')

    def invoke(self, command):
        payload = {
            "params": command.split(' '),
            #"data" : {}
            "data": {"channel": "DRE51D4EM" }
        }
        return self.lambda_graph.invoke(payload)

    def test_invoke(self):
        assert self.invoke('')[0] == '*Here are the `graph` commands available:*'


    def test_invoke_raw_data(self):
        graph_name = 'graph_J2O'
        payload = {'params': ['raw_data', graph_name, 'details'], 'data': {}}
        self.result = Lambda('osbot_jira.lambdas.graph').invoke(payload)

    def test_invoke___last(self):

        assert "| #  |    who    | nodes | edges | " in self.invoke('last 20')[0].get('text')

    def test_invoke___show_last(self):
        self.invoke('show_last 1')

    def test_invoke___save(self):
        self.invoke('save 1 test-save')

    def test_nodes_add_node(self):
        self.invoke('nodes add_node graph_T28 RISK-443')

    def test_nodes_add_edge(self):
        self.invoke('nodes add_edge graph_WLA GSP-1 connects_to GSP-95')

    def test_story__id_stakeholders(self):
        self.invoke('story sec-47-up stakeholders')

    def test_story__story_id___stakeholder___stakeholder_id(self):
        self.invoke('story sec-47-up stakeholder GSP-1 2')


    def test_story__story_id___stakeholder___stakeholder_id__babel_admins(self):
        self.invoke('story babel-admin-vuln stakeholder GSP-4 2')


    def test_expand___abc(self):
        Dev.print(self.invoke('expand abc'))

    def test_raw_data(self):
        result = self.invoke('raw_data graph_J2O details')
        Dev.print(result)

    def test_raw_data__details(self):
        result = self.invoke('raw_data graph_MKF')
        Dev.print(result)

    def test_raw_data__issue_id(self):
        result = self.invoke('raw_data GSSP-111 details')
        Dev.print(result)