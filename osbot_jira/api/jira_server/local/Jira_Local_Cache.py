import osbot_jira
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, files_list, sub_folders, folders_names, folder_create, parent_folder, \
    file_name, file_extension
from osbot_utils.utils.Json import json_load_file, json_save_file
from osbot_utils.utils.Misc import list_set

DEFAULT_JIRA_LOCATION       = '../_jira_backup'
FOLDER_NAME_ISSUES          = 'issues'
FOLDER_NAME_CACHE           = 'cache'
FOLDER_NAME_METADATA        = 'metadata'
FILE_NAME_STATS             = 'backup_stats.json'
FILE_NAME_CACHE_ALL_ISSUES  = 'cache_all_issues.json'

class Jira_Local_Cache:

    def __init__(self):
        #self.folder_osbot_jira    = osbot_jira.__path__.pop()
        self.folder_osbot_jira    = parent_folder(osbot_jira.__file__)
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


    def cache_create_all_issues(self, print_message=False):
        issues = self.load_all_issues()
        json_save_file(python_object=issues, path=self.path_cache_all_issues())
        if print_message:
            print(f"Re-created cache with {len(issues)} issues")
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
            try:
                if file_extension(path_issue_file) == ".json":
                    issue = json_load_file(path_issue_file)
                    issues.append(issue)
            except UnicodeDecodeError as error:
                print(f"[Jira_Local_Cache][load_all_issues] Failed to open file: {path_issue_file}")
        return issues

    @index_by
    def all_issues(self):
        return self.cache_get_all_issues()

    def all_issues_ids(self):
        return list_set(self.all_issues(index_by='Key'))
