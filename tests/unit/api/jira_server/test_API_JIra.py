
import  unittest
from osbot_jira.api.jira_server.API_Jira import API_Jira
from osbot_utils.utils.Dev import Dev


class Test_API_Jira(unittest.TestCase):


    def setUp(self):
        self.api = API_Jira()

    # check connection

    def test_jira_server_info(self):
        jira = self.api.jira()
        assert jira.server_info().get('version') == '7.5.0'

    def test_jira(self):
        jira = self.api.jira()
        assert jira.__class__.__name__ == 'JIRA'
        assert jira.current_user()     == 'gsbot'

    # methods

    def test_covert_issue(self):
        raw_issue = self.api.jira().issue('TASK-502')  # 'FACT-10') #
        issue = self.api.convert_issue(raw_issue)
        Dev.pprint(issue)
        # raw_issue = self.api.jira().issue('SEC-9195')# 'FACT-10') #
        # issue     = self.api.convert_issue(raw_issue)
        # self.api.convert_issue(self.api.jira().issue('SEC-9195'))
        # assert issue['Labels'   ] == ['SEC-9195', 'SEC-9195-CFO']       # check the fields added recently
        # assert issue['Priority' ] == 'Minor'
        #
        # raw_issue = self.api.jira().issue('GSOKR-900')                  # check epic link
        # issue = self.api.convert_issue(raw_issue)
        # assert issue['Epic Link'] == 'GSOKR-924'
        #
        # raw_issue = self.api.jira().issue('GSOKR-872')                  # check parent (for sub taks)
        # issue = self.api.convert_issue(raw_issue)
        # assert issue['Parent'] == 'GSOKR-279'
        # #Dev.pprint(issue)

    def test_fields(self):
        fields = self.api.fields()
        assert len(fields) > 10
        # data   = {}
        # for field in fields:
        #     data[field['name']] = field
        # print()
        # print('|--------------------------------------------------------------------------------------------------|')
        # print('|    name                                                 |             id            |   custom   |')
        # print('|--------------------------------------------------------------------------------------------------|')
        # for name in sorted(set(data.keys())):
        #     field = data[name]
        #     print('| {0:55} | {1:25} | {2:10} |'.format(field['name'], field['id'], str(field['custom'])))


    def test_fields_by_name(self):
        fields_by_name = self.api.fields_by_name()
        assert len(set(fields_by_name)) > 300

    @unittest.skip('this needs to be fixed top reflect the latest added fields')
    def test_issue(self):
        issue = self.api.issue('RISK-1083')

        assert issue == { 'Components'       : []                                           ,
                          'Issue Type'       : 'Risk'                                       ,
                          'Issue Links'      : []                                           ,
                          'Key'              : 'RISK-1083'                                  ,
                          'Issue Links'      : {
                                                  'RISK-1060' : { 'Direction'    : 'Inward'               ,
                                                                 'Issue Type'   : 'Risk'                  ,
                                                                 'Link Type'    : 'is blocked by'         ,
                                                                 'Priority'     : 'Minor'                 ,
                                                                 'Status'       : 'Fixed'                 ,
                                                                 'Summary'      : 'Test Risk'            },
                                                  'RISK-45' :   { 'Direction'    : 'Outward'               ,
                                                                 'Issue Type'   : 'Risk'                  ,
                                                                 'Link Type'    : 'is child of'           ,
                                                                 'Priority'     : 'High'                  ,
                                                                 'Status'       : 'Fixed'                 ,
                                                                 'Summary'      : 'Test issue creation'  },
                                                  'RISK-32' :   { 'Direction'    : 'Outward'              ,
                                                                 'Issue Type'   : 'Risk'                  ,
                                                                 'Link Type'    : 'relates to'            ,
                                                                 'Priority'     : 'Medium'                ,
                                                                 'Status'       : 'Fixed'                 ,
                                                                 'Summary'      : 'TEST'                }},
                          'Rating'           : 'To be determined'                           ,
                          'Risk Description' : 'This is an description'                     ,
                          'Risk Owner'       : 'Dinis Cruz'                                 ,
                          'Status'           : 'Fixed'                                      ,
                          'Summary'          : 'Test risk to GS-Bot'                        }


    def test_issue_add_link__error(self):
        try:
            Dev.pprint(self.api.issue_add_link('from','link_type', 'to'))
        except Exception as error:
            assert error.text == "No issue link type with name 'link_type' found."

    @unittest.skip('needs to be refactored (this method will get the change log for the issues')
    def _test_issue_change_log_only_status(self):
        statuses = self.api.issue_changes_log_only_status("Project=VULN", 300)

        Dev.pprint(statuses)
        #Dev.pprint(list(set(types)))

    def test_issue_update(self):
        issue_data = { "Key"             : "RISK-12"            ,
                       "Summary"         : "new summary value"  ,
                       "Risk Description": "el risk description",
                       "Description"     : "the description"    }
                       #"Risk Rating"     : "Low"                }
                       #"Status"          : "Blocked"            ,}


        result = self.api.issue_update(issue_data)
        Dev.pprint(result)


    # def test_issues_updated_in_last_hour(self):
    #     results    = self.api.issues_updated_in_last_hour()
    #     assert len(results) > 0
    #     #
        # results_1h = self.api.issues_updated_in_last_hour(1)
        # results_10h = self.api.issues_updated_in_last_hour(10)
        # assert results               ==  results_1h
        # assert set(results_1h)       == {'FACT-13', 'RISK-1597'}
        # assert len(set(results_10h)) == 19

    # def test_issues_updated_in_last_day(self):
    #     results = self.api.issues_updated_in_last_day()
    #     assert len(set(results)) > 1
    #     #Dev.pprint(len(set(results)))

    def test_projects(self):
        results =  self.api.jira().projects()
        assert len(results) > 100

    def test_search(self):
        issues = self.api.search('labels=R1')
        assert issues['RISK-1592']['Summary'] == '6 - Risk to Brand'
        assert len(set(issues)) == 6

    def test_search_just_return_keys(self):
        keys = self.api.search_just_return_keys('labels=R1')
        assert keys == ['RISK-1592', 'RISK-1534', 'RISK-1498', 'RISK-1496', 'RISK-1495', 'RISK-1494']
        #keys = self.api.search_just_return_keys('project=RISK')
        #assert len(set(keys)) > 100


    def test_covert_issue_vuln_priority(self):
        assert self.api.issue('VULN-1205').get('VULN Priority') == 'P3'
        assert self.api.issue('VULN-1624').get('VULN Priority') is None
