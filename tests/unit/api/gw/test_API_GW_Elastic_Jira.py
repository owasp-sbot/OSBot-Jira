from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_jira.api.gw.GW_Elastic_Jira import GW_Elastic_Jira


class test_GW_Elastic_Jira(Test_Helper):

    def setUp(self):
        super().setUp()
        self.gw_elastic_jira = GW_Elastic_Jira().setup()


    def test_re_create_index(self):
        self.result = self.gw_elastic_jira.re_create_index()

    def test_send_data_from_all_projects(self):
        #self.result = self.gw_elastic_jira.send_data_from_project('PERSON')
        #self.result = self.gw_elastic_jira.send_data_from_project('Question')
        self.result = self.gw_elastic_jira.send_data_from_project('',0,10000)

    def test_query(self):
        self.result =  len(self.gw_elastic_jira.api_Jira.search('',0,1000))

