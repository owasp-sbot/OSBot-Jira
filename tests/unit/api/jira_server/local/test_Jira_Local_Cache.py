import imp
from importlib.util import find_spec
from unittest import TestCase

import osbot_jira
from osbot_jira.api.jira_server.local.Jira_Local_Cache import Jira_Local_Cache
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists
from osbot_utils.utils.Json import json_load_file
from osbot_utils.utils.Misc import list_set


class test_Jira_Local_Folder(TestCase):

    def setUp(self) -> None:
        self.jira_local_folder = Jira_Local_Cache()

    def test__init__(self):
        assert folder_exists(self.jira_local_folder.folder_osbot_jira   )
        assert folder_exists(self.jira_local_folder.folder_jira         )
        assert folder_exists(self.jira_local_folder.folder_jira_issues  )
        assert folder_exists(self.jira_local_folder.folder_jira_metadata)

    def test_cache_create_all_issues(self):
        self.jira_local_folder.cache_create_all_issues()
        issues = self.jira_local_folder.cache_get_all_issues()
        assert len(issues) > 0

    def test_cache_get_all_issues(self):
        issues = self.jira_local_folder.cache_get_all_issues()
        assert len(issues) > 1500
        assert 'Key' in list_set(issues[0])

    def test_paths_issue_file(self):
        result = self.jira_local_folder.paths_issue_file()
        assert len(result) > 0
        assert 'Key' in list_set(json_load_file(result.pop()))

    def test_load_all_issues(self):
        self.jira_local_folder.load_all_issues()

    def test_projects(self):
        result = self.jira_local_folder.projects()
        assert len(result) > 0
        #pprint(result)

