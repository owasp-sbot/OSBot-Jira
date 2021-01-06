
import unittest

from gw_bot.Deploy import Deploy
from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_utils.utils.Dev import Dev

from osbot_jira.api.GS_Bot_Jira                 import GS_Bot_Jira
from osbot_aws.apis.Lambda import Lambda


class test_GS_Bot_Jira(Test_Helper):
    def setUp(self):
        super().setUp()
        self.api     = GS_Bot_Jira()
        self.channel = 'DDKUZTK6X'                  # gsbot
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_update_lambda(self):
        Deploy().deploy_lambda__jira('osbot_jira.lambdas.jira')

    def test_handle_request(self):
        event = {}
        result = self.api.handle_request(event)
        assert result == {  'attachments': [],
                            'text': ':point_right: no command received, see `jira help` for a list of '
                            'available commands`'}

    def test_handle_request___no_command(self):
        result = self.api.handle_request({})
        assert result == { 'attachments': [],
                           'text': ':point_right: no command received, see `jira help` for a list of available commands`'}

    def test_handle_request___issue_no_id(self):
        result = self.api.handle_request( { "params" : ["issue"] } )
        assert result == {'attachments': [], 'text': ':exclamation: you must provide an issue id '}

    def test_handle_request___issue_bad_id(self):
        result = self.api.handle_request( { "params" : ["issue", "AAAA"] } )
        assert result == {  'attachments': [],
                            'text': '....._fetching data for '
                            '*<https://glasswall.atlassian.net/browse/AAAA|AAAA>* _from index:_ *jira*'}


    def test_cmd_add_link(self):
        params = ['issue','SEC-12104','SEC-12103', 'is parent of']
        self.result = self.api.cmd_add_link(params)


    def test_cmd_create(self):
        params = ['create','TAskasd', 'an new','task']
        self.result = self.api.cmd_create(params)
        #self.result = self.api.cmd_create(params)



    def test_cmd_created_in_last(self):
        params = ['', "20h"]
        result = self.api.cmd_created_in_last(params)
        assert ':point_right: Elk search had ' in result.get('text')

    def test_cmd_created_between(self):
        params = ['', "now-24h","now"]
        result = self.api.cmd_created_between(params)
        assert ':point_right: Elk search had ' in result.get('text')


    def test_cmd_issue(self):
        self.test_update_lambda()
        #self.test__update_lambda_slack_actions()
        #self.result = self.api.cmd_issue(['issue', 'Task-66a'],channel='DRE51D4EM')
        self.result = self.api.cmd_issue(['issue', 'Task-66'])
        #slack_message(self.result.get('text'), self.result.get('attachments'),'DDKUZTK6X', 'T7F3AUXGV')



    def test_cmd_screenshot(self):
        result = self.api.cmd_screenshot(['screenshot', 'VP-1', '2000', '500', '2'], channel='DRE51D4EM')
        Dev.pprint(result.get('text'))

    def test_cmd_links(self):
        self.result = self.api.cmd_links(['links', 'PERSON-1', '1'],channel='DRE51D4EM')

        #assert ' "target": "SEC-10965",\n' in result.get('text')

    def test_cmd_links_Save_Graph_False(self):
        graph = self.api.cmd_links(['links', 'SEC-10965', 'all', '1'],save_graph=False)
        assert len(graph.nodes) > 5

    def test_cmd_links__no_channel(self):
        result = self.api.cmd_links(['links', 'IA-403', 'down', '0'], None, None)
        assert '"target": "IA-403",\n' in result.get('text')

    def test_cmd_links__only_create(self):
        result = self.api.cmd_links(params=['links', 'IA-403', 'down', '0'], only_create=True)
        assert len(result) == 5

    def test_cmd_help(self):
        result = self.api.cmd_help()
        assert result == { 'attachments': [ { 'actions': [],
                                              'callback_id': '',
                                              'color': 'good',
                                              'fallback': None,
                                              'text': ' • created_between\n'
                                                      ' • created_in_last\n'
                                                      ' • diff_sheet\n'
                                                      ' • down\n'
                                                      ' • help\n'
                                                      ' • issue\n'
                                                      ' • links\n'
                                                      ' • load_sheet\n'
                                                      ' • search\n'
                                                      ' • server\n'
                                                      ' • sync_sheet\n'
                                                      ' • table\n'
                                                      ' • up\n'
                                                      ' • updated_in_last\n'
                                                      ' • version\n'}],
                            'text': '*Here are the `jira` commands available:*'}

    # def test_cmd_server(self):
    #     result = self.api.cmd_server(['server','status'])
    #     assert result == { 'attachments': [], 'text': '{\n    "status": "OK 12345"\n}\n'}
    #
    #
    # def test_cmd_up(self):
    #     result = self.api.cmd_up(['links', 'IA-404', '2'], team_id='T7F3AUXGV', channel='GDL2EC3EE')
    #     assert result == None # see data in channel
    #
    # def test_cmd_down(self):
    #     result = self.api.cmd_down(['links', 'IA-404', '2'], team_id='T7F3AUXGV', channel='GDL2EC3EE')
    #     assert result == None  # see data in channel
    #
    # @unittest.skip('long running test (move to sheets test)')
    # def test_cmd_sync_sheet(self):
    #     file_id = '1MHU2Av4tI0FaktjWjbIpFH_zwb-804CAn-MQLuqaq1A'
    #     result = self.api.cmd_sync_sheet(['', file_id], team_id='T7F3AUXGV', channel='GDL2EC3EE')
    #     Dev.pprint(result)



    def test_cmd_search(self):
        params = ['']
        self.result = self.api.cmd_search(params)



    # test via lambda

    @unittest.skip('fix lambda target location')
    def test__cmd_links__via_lambda(self):
        elastic_jira = Lambda('osbot_jira.lambdas.jira')
        payload = {"params": ["links","FACT-47", "up", "3"], "channel": "GDL2EC3EE"}

        result = elastic_jira.invoke(payload)

        text        = result['text']
        attachments = result['attachments']
        channel     = 'GDL2EC3EE'
        slack_message(text, attachments,channel)

        assert ":point_right: Rendering graph for `FACT-47` in the direction `up`, with depth `3`, with plantuml size:" in text

    def test__cmd_server__via_lambda(self):
        elastic_jira = Lambda('osbot_jira.lambdas.jira')
        payload = {"params": ["server", "status"], "channel": "DDKUZTK6X", 'team_id': 'T7F3AUXGV'}

        result = elastic_jira.invoke(payload)
        assert result == {'attachments': [], 'text': '{\n    "status": "OK 12345"\n}\n'}




    # Regression tests

    def test__cmd_links__unhandled_int_int(self):
        result = self.api.cmd_links(['links', 'SEC-10965', '1','all'])  #was : ValueError("invalid literal for int() with base 10: 'all'",)
        assert result == { 'attachments': [],
                           'text': ':red_circle: error: invalid value provided for depth `all`. It must '
                                   'be an number'}



