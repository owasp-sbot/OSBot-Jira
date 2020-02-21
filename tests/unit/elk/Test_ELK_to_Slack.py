from unittest import  TestCase

from osbot_aws.apis.Lambda import Lambda
from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_jira.api.elk.Elk_To_Slack import ELK_to_Slack


class Test_ELK_to_Slack(TestCase):
    def setUp(self):
        self.elk_to_slack = ELK_to_Slack()
        self._lambda      = Lambda("osbot_jira.lambdas.elk_to_slack")

    # def test_update_lambda(self):
    #     Lambda("lambdas.gs.elk_to_slack").update_with_src()
    #     #Lambda('osbot_jira.lambdas.jira').update_with_src()


    def test_cmd_search(self):
        params  = ['Issue\ Type:"Security Controls"']
        user    = 'unit test'
        channel = 'DDKUZTK6X'
        assert len(self.elk_to_slack.cmd_search(params, user, channel)) > 10

    def test_cmd_search___people(self):
        params  = ['people', 'dinis']
        assert self.elk_to_slack.cmd_search(params)[0].get('Key') == 'GSP-95'

    def test_cmd_search__no_params(self):
        params  = []
        response = self.elk_to_slack.cmd_search(params)
        #Dev.print(response)

    def test_cmd_search__view_handle_lambda_event(self):
        params = {'params': ['search', '"GSOKR-924"'], 'user': 'U7ESE1XS7', 'channel': 'DDKUZTK6X'}
        #Dev.pprint(self.elk_to_slack.handle_lambda_event(params))


    def test_get_search_query(self):
        assert self.elk_to_slack.get_search_query([]) == ''
        assert self.elk_to_slack.get_search_query(['people','123']) == 'Issue\\ Type:People AND Summary:123'
        assert self.elk_to_slack.get_search_query(['aaa', '123']) == 'aaa 123'



    def test__lambda_update_invoke(self):
        params =  {'params': ['search', 'project:RISK', 'and', 'Status=Open'], 'user': 'U7ESE1XS7', 'channel': 'DDKUZTK6X'}
        result = self._lambda.invoke(params)
        #Dev.pprint(result)


    def test__cmd_search__via_lambda(self):
        query =  ['Project:RISK', 'AND', 'Status:Open']
        payload = {"params": ["search"] + query, "channel": "DDKUZTK6X"}

        result = self._lambda.invoke(payload)
        assert len(result) > 12


    def test__cmd_search__via_lambda___Epic_issue(self):
        query =  ['"GSOKR-924"']
        payload = {"params": ["search"] + query, "channel": "DDKUZTK6X"}

        result = self._lambda.invoke(payload)
        assert len(result) > 12

    # def test__cmd_search_graph__via_lambda(self):
    #
    #     query =  ['Labels:R1']
    #     payload = {"params": ["search-graph"] + query, "channel": "DDKUZTK6X"}
    #
    #     result = self._lambda.invoke(payload)
    #     Dev.pprint(result)
    #     #assert result is None

    def test___cmd_search_graph__send_results_to_Lambda(self):
        slack_cmd = 'links RISK-1534,RISK-1496,RISK-1498,RISK-1494,RISK-1592,RISK-1495 down 1'
        params    = slack_cmd.split(' ')
        user_id   = None
        channel   = 'DDKUZTK6X'
        result    = Lambda('osbot_jira.lambdas.jira').invoke({"params": params,  "user": user_id, "channel": channel})
        ##Dev.pprint(result)
        slack_message(result.get('text'), result.get('attachments'), channel)

    def test_bug_in_search(self):
        query = ['"Epic Link":“SEC-9700”']
        payload = {"params": ["search"] + query}

        result = self._lambda.invoke(payload)
        #Dev.pprint(result)

