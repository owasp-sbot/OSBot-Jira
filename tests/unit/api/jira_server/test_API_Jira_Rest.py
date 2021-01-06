from osbot_utils.utils.Dev import Dev

from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest


class Test_API_Jira_Rest(Test_Helper):

    def setUp(self):
        super().setUp()
        self.api = API_Jira_Rest()

    def test_config(self):
        assert self.api.config()[1] == 'gsbot'

    def test_fields(self):
        assert len(self.api.fields()) > 10
        #self.result = self.api.fields(index_by='name')
        # for field in self.api.fields():
        #     print(field.get('id'), field.get('name'))

    def test_fields_by_id(self):
        assert 'worklog' in self.api.fields_by_id().keys()
        #Dev.pprint(self.api.fields_by_id())

    def test_fields_by_name(self):
        assert 'Description' in self.api.fields_by_name().keys()
        #Dev.pprint(self.api.fields_by_name())

    # def test_fields_by_name__performance_test(self):        # test what happens when this method is called multiple times
    #     for i in range(0,2):
    #         Dev.pprint(len(self.api.fields_by_name()))


    def test_issue_raw(self):
        issue_id= 'PERSON-1'
        result = self.api.issue_raw(issue_id,'_')
        assert set(result) == {'id', 'self', 'key', 'expand'}

    def test_issue(self):
        issue_id= 'RISK-1'
        result = self.api.issue(issue_id)
        assert 'Key' in set(result)
        #assert set(result) == { 'Assignee', 'Created', 'Creator', 'Description', 'Issue Type', 'Key', 'Labels', 'Last Viewed', 'Priority', 'Project', 'Reporter', 'Risk Description', 'Risk Owner', 'Risk Rating', 'Risk Title', 'Status', 'Summary', 'Updated', 'Work Ratio'}

    def test_issues(self):
        issues_ids = ['RISK-12','RISK-424','SL-118','IA-12']
        result = self.api.issues(issues_ids,'key')
        assert len(result) == 4

    def test_issue_update_field(self):
        issue_id = 'RISK-12'
        summary = 'updated via a rest put request.....'
        result = self.api.issue_update_field(issue_id, 'summary', summary)
        Dev.pprint(result)

    def test_issue_update_fields(self):
        issue_id = 'RISK-12'
        fields = {  "Summary"         : "update from test... 12345"  ,
                    "Description"     : "The description.....123456" ,
                    "Risk Description": "The risk description"       ,
                    "Labels"          : "Risk,Unit-Test"             ,
                    #"Priority"        : "Major"                     ,  # cannot be set (I think it is a screen issue)
                    "Risk Rating"     : "High"                       ,
                    "Assignee"        : "james.wharton"               }
        assert self.api.issue_update_fields(issue_id, fields) is True

    def test_issue_status_available(self):
        issue_id = 'RISK-12'
        result = self.api.issue_status_available(issue_id)
        assert 'Blocked' in set(result)

    def test_projects(self):
        self.result = self.api.projects()

    def test_projects_icons(self):
        self.result = self.api.projects_icons()


    def test_search(self):
        jql         = 'PROJECT=PERSON'
        fetch_all   = True
        issues = self.api.search(jql,fetch_all)

        self.result = len(issues)

    def test_webhook_failed(self):
        self.result = self.api.webhook_failed()

    # https://glasswall.atlassian.net/browse/BUG-162
    # GWBot bug : The Creator field is not currently being updated when importing into elastic
    def test_bug_162__creator_field_not_updated(self):
        #assert self.api.issue_raw('TASK-21').get('fields').get('creator') is not None  # confirms we are getting the value from Jira
        #assert self.api.issue('TASK-21').get('Creator') is None                        # bug , this value should be set

        #self.result = self.api.issue_raw('TASK-21').get('fields')

        self.result = self.api.issue('TASK-21')



    # @unittest.skip('not working')
    # def _test_issue_update_field___status(self):             # for this to work I believe we need to a) send a transition id , and b) make sure they are one of the ones allowed next
    #
    #     issue_id    = 'RISK-12'                             # see method issue_transition_to
    #
    #     # from api_jira.API_Jira import API_Jira
    #     # jira = API_Jira()
    #     # result = jira.issue(issue_id)
    #     # result = jira.issue_next_transitions(issue_id)
    #     # Dev.pprint(result)
    #
    #     #return
    #
    #     issue_start = self.api.issue(issue_id)
    #     Dev.pprint(issue_id)
    #     #status = issue_start.get('Status')
    #     fields = { 'transition' : 12348 }
    #     result = self.api.issue_update_fields(issue_id, fields)
    #     Dev.pprint(result)
    #
    #
    #
    #
    # #def test_issue_update_field___assignee(self):          # this one is working
    # #def test_issue_update_field___dates(self):             # do this one next
    #
    # # workflows
    #
