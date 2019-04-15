import unittest

from pbx_gs_python_utils.gs.API_Issues import API_Issues
from utils.Dev import Dev


class Test_API_Issues(unittest.TestCase):


    def setUp(self):
        self.key     = 'RISK-1515'
        self.api     = API_Issues()

    def test_epic_issues(self):
        results = self.api.epic_issues('SEC-2024')
        Dev.pprint(list(results))

    def test_issue(self):
        issue = self.api.issue(self.key)
        Dev.pprint(issue)

    def test_issues(self):
        keys = ['RISK-1499', 'RISK-1496', 'AAA']
        #result = self.api.elastic.es.mget(index='jira',
        #                                    doc_type='item',
        #                       body={'ids': keys})
        results = self.api.elastic.get_many(keys)
        #Dev.pprint(results)

    def test_issues_all(self):
        issues = {}
        issues.update(self.api.issues_all('jira'))
        issues.update(self.api.issues_all('it_assets'))
        issues.update(self.api.issues_all('sec_project'))

        assert len(issues)  == 12577
        #Dev.pprint(issues['SEC-9195'])


    def test_issues_created_in_last(self):
        result = self.api.issues_created_in_last("3d")
        assert len(result) > 10

    def test_issues_updated_in_last(self):
        result = self.api.issues_updated_in_last("3d")
        assert len(result) > 10

    def test_issues_created_in_last_nnn(self):
        Dev.pprint(len(self.api.issues_created_in_last_seconds(1 * 24 * 60 * 60)))
        Dev.pprint(len(self.api.issues_created_in_last_minutes(1 * 24 * 60     )))
        Dev.pprint(len(self.api.issues_created_in_last_hours  (1 * 24          )))
        Dev.pprint(len(self.api.issues_created_in_last_days   (1)))
        Dev.pprint(len(self.api.issues_created_in_last_weeks  (1)))
        Dev.pprint(len(self.api.issues_created_in_last_months (1)))
        #Dev.pprint(len(self.api.issues_created_in_last_years  (1)))

    def test_create_issue_table(self):
        table = self.api.create_issue_table('RISK-424')
        table.save_tmp()
        #Dev.print(table.puml)

    def test_labels(self):
        result = self.api.labels()
        assert result['AWSrisk'] == [ 'RISK-884', 'RISK-1023', 'RISK-1088', 'RISK-907', 'RISK-607', 'RISK-960', 'RISK-873']
        assert len(result) == 650

    def test_link_types(self):
        result = self.api.link_types()
        #Dev.pprint(len(result))
        assert len(result) == 65


    def test_keys(self):
        keys = self.api.keys()
        assert 'VULN-10' in keys
        assert len(keys) == 2140

    def test_search(self):
        #self.api.elastic.index = "jira,it_assets"
        result = self.api.search("aw", "Summary", 100)
        #Dev.pprint(result)
        Dev.pprint(len(result))
        result = self.api.search("R1", "Labels", 10)
        #Dev.pprint(result)
        Dev.pprint(len(result))

        result = self.api.search("GSP-95", "Key", 10)
        Dev.pprint(result)

    def test_search_using_lucene(self):
        query = 'Project:RISK AND Status:"Fixed"'
        #query = 'Created:[2018-10-01 TO 2018-12-31]'
        #query = "Labels:R2"
        results = self.api.search_using_lucene(query)

        #for issue in results:
        #    print('{0:10} {1:10} {2:20} {3}'.format(issue.get('Key'), issue.get('Project'),issue.get('Status'),issue.get('Summary')))


        #Dev.pprint(len(results))
        assert len(results) > 200

    # def test_stakeholders(self):
    #     result = self.api.stakeholders()
    #     #Dev.pprint(result)
    #     #Dev.pprint(len(set(result)))

    ### move these to separate analysis file

    def test_graph_issue_links_plant_uml(self):
        puml = self.api.graph_issue_links_plant_uml(self.key)
        puml.save_tmp()
        puml._dev_send_to_slack()






