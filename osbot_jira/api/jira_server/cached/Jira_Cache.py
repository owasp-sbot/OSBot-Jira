from osbot_utils.helpers.Local_Caches import Local_Caches
from osbot_utils.utils.Misc import random_text, random_number, upper

from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest


class Jira_Cache:

    FIELDS_TO_PRESERVE = ['Created', 'Environment', 'Issue Links', 'Issue Type', 'Impact' ,
                          'Key', 'Likelihood', 'Priority', 'Project',
                          'Status', 'Updated', 'created', 'id', 'type', 'size']

    def __init__(self, caches_name=None, randomise_issue=True):
        self.randomise_issue  = randomise_issue
        self.api_jira_rest      = API_Jira_Rest()
        self.caches             = Local_Caches(caches_name=caches_name).setup()
        self.cached_issues      = self.caches.cache("cached_issues")
        self.cached_jql         = self.caches.cache("cached_jql"   )

    def issues(self):
        return self.cached_issues.data()


    def jira_issue(self,issue_id, **kwargs):
        issue = self.api_jira_rest.issue(issue_id,**kwargs)
        if issue == {}:
            return {'Key': issue_id}
        if self.randomise_issue:
            return self.randomize(issue)
        return issue

    def jira_search(self, jql, **kwargs):
        return self.api_jira_rest.search(jql=jql, **kwargs)

    def randomize(self, issue):
        if not isinstance(issue, dict):
            return {}

        def recursive_randomization(data):
            if isinstance(data, dict):
                for key in data.keys():
                    if key not in self.FIELDS_TO_PRESERVE:
                        if isinstance(data[key], (dict, list)):
                            data[key] = recursive_randomization(data[key])
                        else:
                            data[key] = random_text(key.lower())
                    else:
                        data[key] = recursive_randomization(data[key])
            elif isinstance(data, list):
                for item in data:
                    recursive_randomization(item)
            return data

        return recursive_randomization(issue)

    def jql_remove(self, jql):
        self.cached_jql.remove(jql)

    def jqls(self):
        return self.cached_jql.data()


    # these methods are designed to allow a direct replacement of the API_Jira_REST class with this Jira_Cache class

    def issue(self, issue_id, **kwargs):
        issue = self.issues().get(issue_id)
        if issue:
            return issue
        issue = self.jira_issue(issue_id, **kwargs)
        self.issue_save(issue_id, issue)
        return issue

    def issue_create(self, project, issue_type, summary, description=None, extra_fields=None):
        key    = f"{upper(project)}-{random_number()}"
        issue  = { "Key"         :  key         ,
                   "Project"     :  project     ,
                   "Summary"     :  summary     ,
                   "Description" :  description ,
                   "Issue Type"  :  issue_type  }
        if extra_fields:
            issue.update(extra_fields)
        if self.randomise_issue:
            self.randomize(issue)
        self.cached_issues.add(key, issue)
        return {"key": key }                                # make it match the return value of API_Jira_Rest.issue_create

    def issue_exists(self, issue_id):
        return self.cached_issues.has_key(issue_id)

    def issue_update_fields(self, issue_id, fields):
        issue = self.issue(issue_id)
        for key, value in fields.items():
            issue[key] = value
        self.issue_save(issue_id, issue)
        return {}                           # this replicates the behaviour of the API_Jira_Rest.issue_update_fields when the update works

    def issue_save(self,issue_id, issue):
        self.cached_issues.add(issue_id,issue)
        return self

    def issue_delete(self, issue_id):
        return self.cached_issues.remove(issue_id)

    def search(self, jql, **kwargs):
        issues = self.cached_jql.get(jql)
        if issues is None:
            jira_issues = self.jira_search(jql,**kwargs)
            if self.randomise_issue:
                issues = []
                for jira_issue in jira_issues:
                    issues.append(self.randomize(jira_issue))
            else:
                issues = jira_issues
            self.cached_jql.add(jql, issues)
        return issues