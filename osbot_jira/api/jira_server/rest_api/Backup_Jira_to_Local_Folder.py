from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, create_folder, folder_exists, folder_delete_all, \
    folder_delete_recursively, folder_create
from osbot_utils.utils.Json import json_save_file, json_load_file
from osbot_utils.utils.Misc import date_time_now, date_time_now_less_time_delta, date_time_less_time_delta, \
    str_to_date_time, list_set, list_index_by

DEFAULT_BACKUP_LOCATION = '../../../../../_jira_backup'
FILE_NAME_STATS         = 'backup_stats.json'
FILE_NAME_LAST_UPDATE   = 'last_update.json'
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
        json_save_file(python_object=data, path=target_file, pretty=True, sort_keys=True)

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

    def save_all_issues(self):
        self.issues = self.api_jira_rest.search(jql="", max_to_fetch=-1)        # only do this for all issues
        self.save_issues(self.issues)

    def save_issues(self, issues):
        for issue in issues:
            self.save_issue(issue)

    def save_issue(self, issue):
        project_name   = issue.get('Project')
        issue_key      = issue.get('Key')
        project_folder = path_combine(self.issues_folder, project_name)
        file_issue     = path_combine(project_folder, f"{issue_key}.json")
        folder_create(project_folder)               # make sure folder exists
        self.save_as_json(data=issue, target_file=file_issue)

    # todo: add support for incremental backup using changes since last sync (like what happens with the Elastic sync)
    #       the model below actually downloads ALL files which is not effective (only good when wanting to do a full backup)
    def save_jira_data(self):       # executes the entire workflow
        with Duration(print_result=False) as duration:
            self.setup()
            self.save_projects_metadata()
            self.save_all_issues()
        return self.save_stats(duration_seconds = duration.seconds())

    def save_jira_issues_updated_since_last_update(self):
        file_last_update = path_combine(self.target_folder, FILE_NAME_LAST_UPDATE)            # todo refactor to separate method
        last_update = json_load_file(file_last_update)
        query_date  = last_update.get('updated_date')
        if query_date is None:                          # if doesn't exist go back one day
            days    = 1
            hours   = 0
            minutes = 0
            query_date = date_time_now_less_time_delta(days=days, hours=hours, minutes=minutes, date_time_format='%Y-%m-%d %H:%M')
        else:
            date_time = str_to_date_time(query_date)            # do this so that we pick up changes made in the last minute
            query_date = date_time_less_time_delta(date_time, minutes=1,date_time_format='%Y-%m-%d %H:%M')
        return self.save_jira_issues_updated_since(query_date)

    def save_jira_issues_updated_since(self,query_date):
        issues      = self.api_jira_rest.search_updated_since_query_date(query_date)
        issues_keys = list_set(list_index_by(issues, "Key"))
        update_data = { "updated_date": date_time_now()  ,
                        "query_date"  : query_date       ,
                        "issue_count" : len(issues_keys),
                        "issues_ids"  : issues_keys     }
        if len(issues) > 0:
            self.save_issues(issues)
            file_last_update = path_combine(self.target_folder, FILE_NAME_LAST_UPDATE)      # todo refactor to separate method
            self.save_as_json(data=update_data, target_file=file_last_update)
        return update_data
