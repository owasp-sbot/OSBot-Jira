import json
import unittest

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_jira.api.graph.Lambda_Graph_Commands import Lambda_Graph_Commands
from pbx_gs_python_utils.utils.Dev   import Dev
from osbot_aws.apis.Lambda           import Lambda


class Test_Lambda_Graph_Commands(Test_Helper):

    def setUp(self):
        super().setUp()
        self.channel = 'DRE51D4EM'
        #self.team_id = 'T7F3AUXGV'
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_update_lambda(self):
        Deploy().deploy_lambda__jira('osbot_jira.lambdas.graph')

    # def test___update_lambda_function(self):
    #     Lambda('lambdas.gsbot.gsbot_graph').update_with_src()

    # def test_add_node(self):
    #     Lambda_Graph_Commands().add_node(self.team_id, self.channel, ['add_node', 1, 'relates to,has RISK'], None)

    def test_create(self):
        result = Lambda_Graph_Commands().create(self.team_id, self.channel, ['graph_K90', 1, 'relates to,has RISK'], None)
        Dev.pprint(result)

    @unittest.skip
    def test_edit(self):
        graph_name = 'graph_HDF'
        result = Lambda_Graph_Commands().edit(self.team_id, self.channel, [graph_name],None)
        Dev.pprint(result)

    def test_expand(self):
        result = json.loads(Lambda_Graph_Commands().expand(params = ['graph_K90', 1, 'relates to,has RISK']))

        self.result = set(result) == {'puml', 'edges', 'graph_name', 'graph_or_key', 'nodes', 'depth'}

    def test_expand__no_puml(self):
        graph = Lambda_Graph_Commands().expand(params = ['graph_K90', 1, 'relates to,has RISK'],save_graph=False)

        assert len(graph.nodes) > 20

    def test_expand__using_jira_id(self):
        Lambda_Graph_Commands().expand(self.channel, params=['RISK-873', 1, 'is created by VULN,asd,asd'])

    def test_expand__bad_link_type(self):
        Lambda_Graph_Commands().expand(self.channel, params=['graph_K90', 1, 'aaaa'])


    def test_last_10(self):
        Lambda_Graph_Commands().last(None,None, [])

    def test_save(self):
        Lambda_Graph_Commands().save(self.channel, ['aaa','bbb'], None)

    def test_mindmap(self):
        Dev.pprint(Lambda_Graph_Commands().mindmap(self.team_id, self.channel, params=['graph_OJF','200','500']))

    def test_mindmap__for_issue(self):
        Dev.pprint(Lambda_Graph_Commands().mindmap(self.team_id, self.channel, params=['GSCS-14']))

    def test_show(self):
        #Lambda_Graph_Commands().show(self.team_id, self.channel, params=[''])
        #Lambda_Graph_Commands().show(self.team_id, self.channel, params=['asd'])
        Lambda_Graph_Commands().show(self.team_id, self.channel, params=['graph_OJF'])


    def test_show_plantuml(self):
        Lambda_Graph_Commands().show(self.team_id, self.channel, params=['graph_OJF','plantuml'])

    def test_show_go_js(self):
        Lambda_Graph_Commands().show(self.team_id, self.channel, params=['graph_OJF','go_js'])

    def test_epic(self):
        key = 'SEC-9696'
        #key = 'GSOS-181'
        Lambda_Graph_Commands().epic(self.team_id,self.channel, [key], None)

    @unittest.skip
    def test_gs_okrs(self):
        Lambda_Graph_Commands().gs_okrs(self.channel, [], None)

    # def test_gs_stakeholder(self):
    #     params = ['babel-admin-vuln', 'stakeholder', 'GSP-4', '2']
    #     Lambda_Graph_Commands().story(self.channel, params, None)

    def test_view_links(self):
        params = ['graph_3XW', 'links']
        Lambda_Graph_Commands().view(None,None, params, None)

    def test_view_only_one_param(self):
        params = ['sec-9696-down']
        Lambda_Graph_Commands().view(self.channel, params, None)


    def test_plantuml(self):
        params = ['sec-9696-down']
        Lambda_Graph_Commands().plantuml(self.team_id, self.channel, params, None)

    def test_raw_data(self):
        params = ['graph_MKF', 'details']
        self.team_id = None
        self.channel = None
        results = Lambda_Graph_Commands().raw_data(self.team_id, self.channel, params, None)
        Dev.pprint(results)
        #results = Lambda_Graph_Commands().raw_data(self.team_id, self.channel, ['aaa'], None)
        Dev.print(results)

    def test_raw_data__issue_id(self):
        params = ['GSSP-111', 'details']        # when an issue ID is passed we should get the value as the first node
        self.team_id = None
        self.channel = None
        results = Lambda_Graph_Commands().raw_data(params=params)
        assert results['nodes']['GSSP-111']['Creator'] == 'dinis.cruz'



