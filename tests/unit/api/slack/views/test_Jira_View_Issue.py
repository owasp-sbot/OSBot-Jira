from unittest import TestCase
from pbx_gs_python_utils.utils.Dev import Dev
from osbot_jira.Deploy import Deploy
from osbot_jira.api.slack.views.Jira_View_Issue import Jira_View_Issue


class test_Jira_View_Issue(TestCase):
    def setUp(self):
        self.jira_view_issue          = Jira_View_Issue()
        self.lambda_name_jira_actions = 'osbot_jira.lambdas.slack_actions'
        self.result                   = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__update_lambda_all(self):
        self.test__update_lambda_elastic_jira()
        self.test__update_lambda_slack_actions()
        self.test_updata_lambda_slack_jira_actions()

    def test__update_lambda_elastic_jira(self):
        Deploy('osbot_jira.lambdas.elastic_jira').deploy()             # update the main jira lambda

    def test__update_lambda_slack_actions(self):
        Deploy('osbot_jira.lambdas.slack_actions').deploy()            # update the lambda that handles the callbacks

    def test_updata_lambda_slack_jira_actions(self):
        Deploy('osbot_jira.lambdas.slack_jira_actions').deploy()    # used for dialog submissions

    def test_create_and_send(self):
        self.test__update_lambda_slack_actions()
        self.jira_view_issue.issue_id = 'GSCS-372' #RISK-1524' #''SEC-11961'
        self.jira_view_issue.channel  = 'DDKUZTK6X'
        self.jira_view_issue.team_id  = 'T7F3AUXGV'
        self.result = self.jira_view_issue.create_and_send()


    def test_add_select_with_issue_links(self):
        #self.test__update_lambda_slack_actions()
        issue_id = 'GSCS-372'
        issue_id = 'GSCS-1'
        self.jira_view_issue.channel = 'DDKUZTK6X'
        self.jira_view_issue.team_id = 'T7F3AUXGV'
        self.jira_view_issue.load_issue(issue_id).add_select_with_issue_links()
        self.result                 = self.jira_view_issue.send()

        #self.result = self.jira_view_issue.issue_links({'value':'GSCS-372'})

    def test_create_ui_actions_with_transitions(self):
        issue_id       = 'GSCS-372'
        #issue_id       = 'SEC-9892'
        current_status = 'Backlog'
        self.jira_view_issue.channel  = 'DDKUZTK6X'
        self.jira_view_issue.team_id  = 'T7F3AUXGV'
        self.result = self.jira_view_issue.create_ui_actions_with_transitions(issue_id, current_status)

    def test_create_ui_edit_issue_field(self):
        self.test__update_lambda_slack_actions()
        self.test_updata_lambda_slack_jira_actions()
        self.jira_view_issue.issue_id = 'GSCS-372'
        self.jira_view_issue.channel = 'DDKUZTK6X'
        self.jira_view_issue.team_id = 'T7F3AUXGV'
        self.result = self.jira_view_issue.create_ui_edit_issue_field()

    def test_view_links(self):
        self.jira_view_issue.channel = 'DDKUZTK6X'
        self.jira_view_issue.team_id = 'T7F3AUXGV'
        self.result = self.jira_view_issue.view_links({'value':'GSCS-32'})