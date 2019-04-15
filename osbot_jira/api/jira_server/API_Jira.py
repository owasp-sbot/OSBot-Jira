
from jira import JIRA
from osbot_aws.apis.Secrets import Secrets

from pbx_gs_python_utils.utils.Lambdas_Helpers import log_info, log_error

# to add
#  jira().groups
#  jira(),group_members
#  jira().search_users
#       users = jira._jira.search_users("%", maxResults = 1000)  # works in cloud server
#       users = jira._jira.search_users(".", maxResults = 1000)  # works in hosted server


class API_Jira:
    def __init__(self):
        self.secrets_id = 'GS_BOT_GS_JIRA'
        self._jira      = None
        self._fields    = None                  # cache this value per request (since it is expensive and data doesn't change that much)

    #@clear_local_cache_files
    #def clear_local_cache(self):
    #    return self

    # helper methods

    def jira(self):
        if self._jira is None:
            try:
                server, username, password = self.jira_server_details()

                original_fields = JIRA.fields                                               # patch fields function to prevent a call to it on every ctor call
                JIRA.fields     = lambda _self: []                                          # set it to a lambda function that returns an empty array
                self._jira      = JIRA({'server': server}, basic_auth=(username, password))
                JIRA.fields     = original_fields                                           # restore 'fields' method
            except Exception as error:
                print('[API_JIRA] [error creating jira connection]: {0}'.format(error))


        return self._jira

    # main methods


    def convert_issue(self, issue):
        #print('converting issue: {0}'.format(issue))
        def custom_field_value(field_id, field_name = None):
            field_value = issue.raw['fields'].get(field_id)
            if field_value:
                if field_name:
                    return field_value[field_name]
                else:
                    return field_value

        def custom_brands_values():
            brand_value  = issue.raw['fields'].get('customfield_12626')
            brands_value = issue.raw['fields'].get('customfield_12501')
            brands = []
            if brand_value:
                brands.append(brand_value['value'])
            if brands_value:
                for item in brands_value:
                    brands.append(item['value'])
            return list(set(brands))

        def components_values():
            return [i.name for i in issue.fields.components]

        def likelihood():
            value = custom_field_value('customfield_14161' , 'value'       )
            if value:
                value = value.split(':').pop(0)
            return value

        def split(value, separator):
            if value:
                items = value.split(separator)              # split by separator
                return [item.strip() for item in items]     # trim individual results

        data = {    "Assignee"          : custom_field_value('assignee'          , 'name'       ) ,
                    "Brands"            : custom_brands_values()                                  ,
                    "Components"        : components_values()                                                      ,
                    "Created"           : issue.fields.created                                    ,
                    "Creator"           : custom_field_value('creator'           , 'name'       ) ,
                    "Description"       : custom_field_value('description'                      ) ,
                    "Email"             : custom_field_value('customfield_14549'                ) ,
                    'Epic Link'         : custom_field_value('customfield_11200'                ) ,
                    "GDPR Article"      : split(custom_field_value('customfield_14156'),'\r\n'  ) ,
                    "Image Url"         : custom_field_value('customfield_14551'                ) ,
                    "Issue Type"        : custom_field_value('issuetype'         , 'name'       ) ,
                    "Issue Links"       : {}                                                      ,
                    "ISO27001 Standard" : split(custom_field_value('customfield_14157'),','     ) ,
                    "Key"               : issue.key                                               ,
                    "Labels"            : issue.fields.labels                                     ,
                    "Latest_Information": custom_field_value("customfield_12924"                ) ,
                    "Likelihood"        : likelihood()                                            ,
                    "Parent"            : custom_field_value('parent'            , 'key'        ) ,
                    "Priority"          : custom_field_value('priority'          , 'name'       ) ,
                    "Project"           : custom_field_value('project'           , 'name'       ) ,
                    "Slack ID"          : custom_field_value('customfield_14548'                ) ,
                    "Summary"           : custom_field_value('summary'                          ) ,
				    "Status"            : custom_field_value('status'            , 'name'       ) ,
                    #'Subtasks'          : {}                                                      ,
				    "Rating"            : custom_field_value('customfield_12639' , 'value'      ) ,
                    "Reporter"          : custom_field_value('reporter'          , 'name'       ) ,
                    "Risk Owner"        : custom_field_value('customfield_12622' , 'displayName') ,
                    "Updated"           : issue.fields.updated                                    ,
                    "Impacts"           : custom_field_value('customfield_14162' , 'value'       ) }


        for link in issue.fields.issuelinks:
            issue_Link = {}
            if  hasattr(link,"outwardIssue"):
                issue_Link["Link Type" ] = link.type.outward
                issue_Link["Direction" ] = 'Outward'
                link_data                = link.outwardIssue

            if  hasattr(link,"inwardIssue"):
                issue_Link["Direction" ] = 'Inward'
                issue_Link["Link Type" ] = link.type.inward
                link_data                = link.inwardIssue

            issue_Link["Issue Type"] = link_data.fields.issuetype.name
            issue_Link["Id"        ] = link.id
            issue_Link["Key"       ] = link_data.key
            issue_Link["Priority"  ] = link_data.fields.priority.name
            issue_Link["Status"    ] = link_data.fields.status.name
            issue_Link["Summary"   ] = link_data.fields.summary

            if data['Issue Links'].get(link_data.key) is None : data['Issue Links'][link_data.key] = []
            data['Issue Links'][link_data.key].append(issue_Link)


        # for subtask in issue.fields.subtasks:                 # need a better solution to handle subtasks since this is not indexing very well
        #     data['Subtasks'][subtask.key] = {
        #          'Issue Type': subtask.fields.issuetype.name,
        #          'Priority'  : subtask.fields.priority .name,
        #          'Status'    : subtask.fields.status   .name,
        #          'Summary'   : subtask.fields.summary,
        #     }
        return data

    #@use_local_cache_if_available
    def fields(self):
        if self._fields is None:
            self._fields = self.jira().fields()
        return self._fields

    def fields_by_name(self):
        fields = {}
        for field in self.fields():
            name = field.get('name')
            fields[name] = field

        return fields

    def issue_add_comment(self, key, comment):
        self.jira().add_comment(key,comment)
        return self
    def issue_comments(self, key):
        comments = []
        for comment in self.jira().comments(key):
            comments.append({ "author" : comment.author.displayName,
                              "body"   : comment.body,
                              "id"     : comment.id
                              })
        return comments

    def issue_create(self, project, summary, description, issue_type):
        return self.jira().create_issue(project = project, summary=summary, description=description, issuetype={'name': issue_type})

    def issue_delete(self, key):
        issue = self.jira().issue(key, fields=[], expand= False)  # need to double check the performance impact of: fields=[], expand= False
        issue.delete()
        return self

    def issue_add_link(self,from_key, link_type, to_id):
        self.jira().create_issue_link(type = link_type,  inwardIssue = from_key, outwardIssue = to_id)
        return self

    def issue_delete_link(self, link_id):
        self.jira().delete_issue_link(link_id)
        return self

    def issue_links(self,key):
        issue_links = {}
        issue = self.issue(key)
        if issue:
            for key, items in issue.get('Issue Links').items():
                for item in items:
                    link_type = item.get('Link Type')
                    if issue_links.get(link_type) is None : issue_links[link_type] = []
                    issue_links[link_type].append(item)
        return issue_links

    def issue_next_transitions(self,key):
        transitions = {}
        items = self.jira().transitions(key)
        for item in items:
            transitions[item['name']] = item['id']
        return transitions

    def issue_transition_to(self, key, transition_name):
        transitions     = self.issue_next_transitions(key)
        transitions_id  = transitions[transition_name]
        return self.issue_transition_to_id(key, transitions_id)

    def issue_transition_to_id(self, key, transitions_id):
        self.jira().transition_issue(key,transitions_id)
        return self

    def issue_update(self, issue_data):
        fields_by_name = self.fields_by_name()
        key = issue_data.get('Key')
        fields_data = {}
        for name, value in issue_data.items():
            field = fields_by_name.get(name)
            if field:
                field_id = field.get('id')
                if field_id not in ['issuekey']:
                    fields_data[field_id] = value

        # this is VERY slow
        jira = self.jira()
        issue = self.jira().issue(key, fields=['Key'], expand= [])

        issue.self = issue.self.replace('eb.ngrok.io', 'eb.eu.ngrok.io')            # todo: no idea why this is needed

        return issue.update(fields=fields_data)

    #def issue_update(self, key, summary = None, description = None):
    #    issue = self.jira().issue(key, fields=['Key'], expand= [])
    #    return issue.update(summary = summary, description = description)

    def issue_worklogs(self, key):
        return self.jira().worklogs(key)

    #@use_local_cache_if_available
    def issue(self, id):
        return self.issue_no_cache(id)

    def issues(self, ids):
        issues = {}
        for id in ids:
            issue = self.issue_no_cache(id)
            if issue:
                issues[id] = issue
        return issues

    def issue_no_cache(self, id):
        #log_info('Retrieving issue with from Jira with ID: {0}'.format(id),'API_Jira')
        try:
            issue = self.jira().issue(id)
            return self.convert_issue(issue)
        except Exception as error:
            log_error(str(error), 'API_Jira | issue')
        return None

    #@use_local_cache_if_available
    #@save_result_to_local_cache
    def issue_changes_log_only_status(self, jql, start_at = 0, max = -1):
        keys = self.search_just_return_keys(jql)
        if max > 0:
            keys = keys[start_at:max]

        size = len (keys)
        log_info("There are {0} keys to process".format(size), "issue_changes_log_only_status")
        statuses = {}
        for key in keys:
            statuses[key] = self.issue_change_log_only_status(key)
            if len(set(statuses)) % 25 == 0:
                log_info("in {0} out of {1}".format(len(set(statuses)), size))
        log_info("all done", "issue_changes_log_only_status")
        return statuses

    def issue_change_log(self,key):
        change_log = []
        data = self.jira().issue(key, fields=['key'], expand='changelog')
        for history in data.changelog.histories:
            for item in history.items:
                entry = { 'Created'   : history.created     ,
                          'Field'     : item.field          ,
                          'From'      : item.fromString     ,
                          'To'        : item.toString       ,
                          'Entry_Id'  : history.id          }
                if(hasattr(history, "author")):
                    entry['Who'] = history.author.name
                else:
                    entry['Who'] = 'Unassigned'
                change_log.append(entry)

        return change_log

    def issue_change_log_only_status(self,key):
        change_log = []
        data = self.jira().issue(key, fields=['key'], expand='changelog')
        for history in data.changelog.histories:
            for item in history.items:
                if item.field == 'status':
                    entry = { 'Created'   : history.created     ,
                              #'Field'     : item.field          ,
                              'From'      : item.fromString     ,
                              'To'        : item.toString       ,
                              'Entry_Id'  : history.id          }
                    if(hasattr(history, "author")):
                        entry['Who'] = history.author.name
                    else:
                        entry['Who'] = 'Unassigned'
                    change_log.append(entry)

        return change_log


    def issues_updated_in_last_day(self, hour=1):
        return self.search_no_cache('project in (VULN,RISK,SEC,FACT) AND updated >= -{0}d'.format(hour))

    def issues_updated_in_last_hour(self, hour=1):
        return self.search_no_cache('project in (VULN,RISK,SEC,FACT) AND updated >= -{0}h'.format(hour))

    def issues_updated_in_last_minute(self, minute=1):
        return self.search_no_cache('project in (VULN,RISK,SEC,FACT) AND updated >= -{0}m'.format(minute))

    def jira_server_details(self):
        data     = Secrets(self.secrets_id).value_from_json_string()
        server   = data.get('server')
        username = data.get('username')
        password = data.get('password')
        return server, username, password

    def projects(self):
        projects = {}
        for project in self.jira().projects():
            projects[project.key]= project
        return projects

    #@use_local_cache_if_available
    #@save_result_to_local_cache
    def search(self, jql, start_at = 0, max = -1):
        return self.search_no_cache(jql,start_at,max)

    def search_no_cache(self, jql, start_at = 0, max = -1):
        issues = {}
        count = start_at
        if max == -1:
            max_per_query = 500
        else:
            max_per_query = max
        while True:
            print('searching JIRA server for {0} , starting at {1} (for a max of {2})'.format(jql, count, max))
            log_info('searching JIRA server for {0} , starting at {1} (for a max of {2})'.format(jql, count, max))
            data = self.jira().search_issues(jql, startAt=count, maxResults=max_per_query)                           # use the max we can fetch
            log_info('received {0} results from server'.format(len(data)))
            if len(data) == 0:                                                                                       # when we have received all files
                break                                                                                                # break from the while true
            for raw_issue in data:                                                                                   # process data received
                issue = self.convert_issue(raw_issue)                                                                # convert JIRA data into a nice usable python object
                issues[issue['Key']] = issue                                                                         # add mapped issue to issues object
                count += 1                                                                                           # keep track of how many requests we have note (note: check if len(set(issues)) will produce the same thing)
            if max != -1 and max <= count:
                break
            if len(data) < max_per_query:                                                                            # also end if we didn't received max_per_query items
                break
        return issues

    def search_just_return_keys(self, jql, start_at = 0, max = -1):
        keys = []
        count = start_at
        if max == -1:
            max_per_query = 500
        else:
            max_per_query = max
        while True:
            data = self.jira().search_issues(jql, startAt=count, maxResults=max_per_query, fields=['key'])             # this will only return the Key (although I don't this the fields value is working since the data.fields variable is still empty)
            if len(data) == 0:
                break
            for raw_issue in data:
                keys.append(raw_issue.key)
                count += 1                                                                                           # keep track of how many requests we have note (note: check if len(set(issues)) will produce the same thing)
            if max != -1 and max <= count:
                break
            if len(data) < max_per_query:                                                                            # also end if we didn't received max_per_query items
                break
        return keys


    #def run_sql(self, jql):
    #    return None