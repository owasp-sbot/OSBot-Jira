from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_jira.api.jira_server.Jira_Icons import Jira_Icons
from osbot_utils.utils.Files import folder_exists, file_exists


class test_Jira_Icons(Test_Helper):
    def setUp(self):
        super().setUp()
        self.jira_icons = Jira_Icons()

    def test_all_icons_local(self):
        assert len(self.jira_icons.all_icons_local()) > 10

    def test_icon_local_for_key(self):
        assert file_exists(self.jira_icons.icon_local_for_key('RISK-1'))

    def test_icon_local(self):
        assert file_exists(self.jira_icons.icon_local('risk'))
        assert self.jira_icons.icon_local('risk_AAA') is None

    def test_icons_urls(self):
        assert len(self.jira_icons.icons_urls()) > 10

    def test_icons_folder(self):
        assert folder_exists(self.jira_icons.icons_folder())



