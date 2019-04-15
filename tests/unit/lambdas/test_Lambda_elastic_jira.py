import  unittest

from    osbot_aws.apis.Lambda import Lambda
from    pbx_gs_python_utils.utils.Dev         import Dev

from osbot_jira.lambdas.elastic_jira import run


@unittest.skip('lambda not deployed (yet)')
class test_lambda_elastic_jira(unittest.TestCase):
    def setUp(self):
        self.jira_issues = Lambda('osbot_jira.lambdas.elastic_jira')

    def test_invoke_directly(self):
        response = run({},{})
        assert response == { 'attachments': [],
                             'text': ':point_right: no command received, see `jira help` for a list of '
                                      'available commands`'}


    # def test_update(self):
    #     result = self.jira_issues.update_with_lib().invoke()
    #     Dev.pprint(result)



    def test_update_invoke(self):
        #self.jira_issues.update_with_lib()
        key = 'RISK-424'
        issue = self.jira_issues.invoke({"params": ['issue', key], "channel": 'GDL2EC3EE'})
        Dev.pprint(issue)

    def test_update_invoke__link_links(self):
        id = 'RISK-1'
        result = self.jira_issues.invoke({"params": ["issue-links", id], "channel": 'GDL2EC3EE'})
        #Dev.pprint(result)

    def test_update_invoke__link_share(self):
        id = 'RISK-2'
        #issue = self.jira_issues.update_with_src().invoke({"params": ["issue", id], "channel": 'GDL2EC3EE'})
        #issue = self.jira_issues.update_with_src().invoke({"params": ["issue-links", id], "channel": 'GDL2EC3EE'})
        result = self.jira_issues.invoke({"params": [ 'link_shared', '[{"url":"https://jira.photobox.com/browse/SEC-1234"}]'], "channel": 'GDL2EC3EE'})

        #Dev.pprint(result)

    def test_update_invoke__test_cmd(self):
        result = self.jira_issues.invoke({"params": [ 'test'], "channel": 'GDL2EC3EE'})
        #Dev.pprint(result)



    def test_invoke_bad_cmd(self):
        result = self.jira_issues.invoke({"params": ["aaaa"], 'user' : 'abc'})
        assert result == { 'attachments': [],
                          'text': ':red_circle: Not supported command `aaaa` , see all available using `jira help`'}



    # BUG issue doesn't return data
    # def test_invoke__no_data_for_issue(self):
    #     issue_id = 'GSCS-24'
    #     result = self.jira_issues.invoke({"params": ['issue',issue_id], 'team_id':'T7F3AUXGV', 'channel':'GDL2EC3EE' })
    #     Dev.pprint(result)
