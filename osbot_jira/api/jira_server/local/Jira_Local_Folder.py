import osbot_jira
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, files_list, sub_folders, folders_names, folder_create
from osbot_utils.utils.Json import json_load_file, json_save_file

DEFAULT_JIRA_LOCATION       = '../_jira_backup'
FOLDER_NAME_ISSUES          = 'issues'
FOLDER_NAME_CACHE           = 'cache'
FOLDER_NAME_METADATA        = 'metadata'
FILE_NAME_STATS             = 'backup_stats.json'
FILE_NAME_CACHE_ALL_ISSUES  = 'cache_all_issues.json'

class Jira_Local_Folder:

    def __init__(self):
        self.folder_osbot_jira    = osbot_jira.__path__.pop()
        self.folder_jira          = path_combine(self.folder_osbot_jira, DEFAULT_JIRA_LOCATION )
        self.folder_jira_issues   = path_combine(self.folder_jira, FOLDER_NAME_ISSUES    )
        self.folder_jira_metadata = path_combine(self.folder_jira, FOLDER_NAME_METADATA  )
        self.folder_jira_cache    = path_combine(self.folder_jira, FOLDER_NAME_CACHE     )
        self.setup()

    def setup(self):
        folder_create(self.folder_jira          )
        folder_create(self.folder_jira_issues   )
        folder_create(self.folder_jira_metadata )
        folder_create(self.folder_jira_cache    )


    def cache_create_all_issues(self):
        issues = self.load_all_issues()
        json_save_file(python_object=issues, path=self.path_cache_all_issues())
        return self

    def cache_get_all_issues(self):
        return json_load_file(self.path_cache_all_issues())

    def paths_issue_file(self):
        return files_list(self.folder_jira_issues)

    def path_cache_all_issues(self):
        return path_combine(self.folder_jira_cache, FILE_NAME_CACHE_ALL_ISSUES)

    def projects(self):
        return folders_names(sub_folders(self.folder_jira_issues))

    def load_all_issues(self):
        issues = []
        for path_issue_file in self.paths_issue_file():
            issue = json_load_file(path_issue_file)
            issues.append(issue)
        return issues
