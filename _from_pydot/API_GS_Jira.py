from osbot_jira.api.jira_server.API_Jira import API_Jira
from pbx_gs_python_utils.utils.Json             import Json
from pbx_gs_python_utils.utils.Local_Cache      import get_local_cache_path
from pbx_gs_python_utils.utils.Lambdas_Helpers  import log_debug


class API_GS_Jira:
    def __init__(self):
        self.api_Jira = API_Jira()
        self._issues  = None

    #@use_local_cache_if_available
    #@save_result_to_local_cache
    # def issues_gs_projects(self):
    #     issues = {}
    #     issues.update(self.api_Jira.search('project=FACT'))
    #     issues.update(self.api_Jira.search('project=VULN'))
    #     issues.update(self.api_Jira.search('project=RISK'))
    #     # SEC Project is a bit special since it has 8k issues which had to be fetched in blocks of 250
    #     step_by = 500
    #     for i in range(0,18):
    #         start_at = i * step_by
    #         issues.update(self.api_Jira.search('project=SEC', start_at, step_by))
    #
    #     return issues

    # def issue(self, id):
    #     issue = self.issues().get(id)
    #     if issue is None:
    #        print('could not find issue in local cache, so fetching it: {0}'.format(id))
    #        issue = self.api_Jira.issue(id)
    #     return issue
    #
    # def issues(self):
    #     if self._issues is None:
    #         self._issues = self.issues_gs_projects()
    #     return self._issues

    def update_changes_made_last_hour(self, hour=1):
        cache_path    = get_local_cache_path(self, 'issues_gs_projects',[])        # local cache file to update
        changes       = self.api_Jira.issues_updated_in_last_hour(hour)            # get changes
        issues        = self.issues_gs_projects()                                  # get all issues data
        linked_issues = {}
        for key, value in changes.items():                                         # for each item changed
            log_debug('updating issue {0} - {1}'.format(key,value['Summary']))
            issues[key] = value                                                    # update the issue with the new value
            linked_issues.update(value['Issue Links'])                             # capture linked issues that we need to update

        linked_issues = set(linked_issues)
        log_debug('There are {0} linked issues to update: {1}'.format(len(linked_issues), linked_issues))
        # this need improvement since it will take ages when there are lots of updates (for example changes to 180 issues caused 584 issues updates)
        # also I think this is too much since there are only a couple fields in the linked issue data that would need updating (for example the priority)
        for key in linked_issues:
            issues[key] = self.api_Jira.issue_no_cache(key)

        Json.save_json_gz(cache_path, issues)                                       # update cache file
        return (changes,linked_issues)                                              # return changes and linked_issues