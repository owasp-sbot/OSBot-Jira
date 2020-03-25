from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_jira.api.gw.GW_Elastic_Jira import GW_Elastic_Jira


class test_GW_Elastic_Jira(Test_Helper):

    def setUp(self):
        super().setUp()
        self.gw_elastic_jira = GW_Elastic_Jira().setup()


    def test_re_create_index(self):
        self.result = self.gw_elastic_jira.re_create_index()

    def test_send_data_from_one_projects(self):
        self.result = self.gw_elastic_jira.send_data_from_project('KeyResult')

    def test_send_data_from_all_projects(self):
        self.result = self.gw_elastic_jira.send_data_from_project()

    def test_query(self):
        self.result =  len(self.gw_elastic_jira.api_Jira.search('',0,1000))


    def test_reload_all_data_from_jira_project(self):
        self.result = self.gw_elastic_jira.reload_all_data_from_jira_project()