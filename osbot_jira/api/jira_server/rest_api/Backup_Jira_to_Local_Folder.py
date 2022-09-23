from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, create_folder, folder_exists, folder_delete_all, \
    folder_delete_recursively
from osbot_utils.utils.Json import json_save_file
from osbot_utils.utils.Misc import date_time_now

DEFAULT_BACKUP_LOCATION = '../../../../../_jira_backup'
FILE_NAME_STATS         = 'backup_stats.json'
FOLDER_NAME_ISSUES      = 'issues'
FOLDER_NAME_METADATA    = 'metadata'

class Backup_Jira_to_Local_Folder:

    def __init__(self):
        self.api_jira_rest = API_Jira_Rest()
        self.target_folder   = path_combine(__file__, DEFAULT_BACKUP_LOCATION)
        self.issues_folder   = path_combine(self.target_folder, FOLDER_NAME_ISSUES)
        self.metadata_folder = path_combine(self.target_folder, FOLDER_NAME_METADATA)
        self.issues          = []
        self.projects        = []

    def setup(self):
        self.delete_existing_data()
        create_folder(self.target_folder  )
        create_folder(self.issues_folder  )         # delete all issues and folders to that we pick up delete issues
        create_folder(self.metadata_folder)         # git will handle version control
        return self

    def delete_existing_data(self):
        if folder_exists(self.target_folder) and folder_exists(self.issues_folder) and folder_exists(self.metadata_folder):
            folder_delete_recursively(self.issues_folder  )  # delete all issues and metadata folders to that we pick up delete issues
            folder_delete_recursively(self.metadata_folder)  # git will handle version control

    def path_to_project(self, project_name):
        return path_combine(self.issues_folder, project_name)

    # save methods
    def save_as_json(self, data, target_file):
        json_save_file(python_object=data, path=target_file, pretty=True)

    def save_stats(self, duration_seconds=-1):
        stats_data = { "date_backup_created": date_time_now(return_str=True),
                       "issue_count"        : len(self.issues)              ,
                       "project_count"      : len(self.projects)            ,
                       "duration_seconds"   : duration_seconds}

        file_stats = path_combine(self.target_folder, FILE_NAME_STATS)
        self.save_as_json(data=stats_data, target_file=file_stats)
        return stats_data

    def save_projects_metadata(self):
        self.projects = self.api_jira_rest.projects()
        for project_key, project_data in self.projects.items():
            project_name          = project_data.get('name')
            path_to_project       = self.path_to_project(project_name)
            file_project_metadata = path_combine(self.metadata_folder, f"{project_name}.json")

            create_folder(path_to_project)
            self.save_as_json(data=project_data, target_file=file_project_metadata)
        return self

    def save_issues(self):
        self.issues = self.api_jira_rest.search(jql="", max_to_fetch=-1)
        for issue_data in self.issues:
            project_name   = issue_data.get('Project')
            issue_key      = issue_data.get('Key')
            project_folder = path_combine(self.issues_folder, project_name)
            file_issue     = path_combine(project_folder, f"{issue_key}.json")
            self.save_as_json(data=issue_data, target_file=file_issue)
        #pprint(issues)


    def save_jira_data(self):       # executes the entire workflow
        with Duration(print_result=False) as duration:
            self.setup()
            self.save_projects_metadata()
            self.save_issues()
        return self.save_stats(duration_seconds = duration.seconds())