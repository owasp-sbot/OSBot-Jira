from unittest import TestCase

from osbot_jira.api.jira_server.rest_api.Backup_Jira_to_Local_Folder import Backup_Jira_to_Local_Folder
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, file_contents, file_exists


class test_Backup_Jira_to_Local_Folder(TestCase):

    def setUp(self) -> None:
        Setup()
        self.backup_jira = Backup_Jira_to_Local_Folder()

    def test__init__(self):
        pprint(self.backup_jira.target_folder)

    def test_setup(self):
        assert self.backup_jira.setup() == self.backup_jira
        assert folder_exists(self.backup_jira.target_folder)
        assert folder_exists(self.backup_jira.issues_folder)
        assert folder_exists(self.backup_jira.metadata_folder)

    def test_save_stats(self):
        self.backup_jira.save_stats()


    def test_save_projects_metadata(self):
        self.backup_jira.save_projects_metadata()

    def test_save_issues(self):
        self.backup_jira.save_issues()

    def test_save_jira_data(self):
        stats_data = self.backup_jira.save_jira_data()
        pprint(stats_data)