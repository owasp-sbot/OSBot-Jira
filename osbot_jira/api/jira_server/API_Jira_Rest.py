import json

import requests

from osbot_aws.helpers.Lambda_Helpers import log_error
from osbot_aws.apis.Secrets import Secrets                                  # todo: refactor this out of this class (so that we don't have a dependency in AWS
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import Dev, pprint
from osbot_utils.utils.Json import json_dumps
from osbot_utils.utils.Lists import list_chunks
from osbot_utils.utils.Misc import env_vars, list_set


class API_Jira_Rest:
    def __init__(self):
        self.secrets_id    = 'GS_BOT_GS_JIRA'
        self.jira_env_vars = {'JIRA_API_EMAIL', 'JIRA_API_TOKEN', 'JIRA_API_SERVER'}
        self._config       = None
        self._fields       = None               # cache this value per request (since it is expensive and data doesn't change that much)
        self.log_requests  = False

    def config(self):
        if self._config is None:
            if set(self.jira_env_vars).issubset(set(env_vars())):
                self._config = self.config_using_env_vars()
            else:
                self._config = self.config_using_aws_secrets()

        return self._config

    def config_using_aws_secrets(self):
        data = Secrets(self.secrets_id).value_from_json_string() or {}
        return (data.get('server'), data.get('username'), data.get('password'))


    def config_using_env_vars(self):
        vars     = env_vars()
        username = vars.get('JIRA_API_EMAIL')
        password = vars.get('JIRA_API_TOKEN')
        server   = vars.get('JIRA_API_SERVER')
        return (server, username, password)

    def set_public_jira(self, server):
        self._config = (server, "", "")
        return self

    # request helpers

    def request_get(self,path):
        return self.request_method('GET', path)

    def request_delete(self,path):
        return self.request_method('DELETE', path)

    def request_method(self,method, path, data=None):
        (server, username, password)= self.config()
        if server is None:
            return None
        if path.startswith('http') is False:
            if server.endswith('/') is False:
                server +='/'
            path = '{0}rest/api/2/{1}'.format(server, path)
        #print(path)
        if self.log_requests: Dev.pprint('get', path)
        if username and password:
            if method =='GET':
                response = requests.get(path, auth=(username, password))
            elif method == 'POST':
                json_data = json_dumps(data or {})
                headers   = {'Content-Type': 'application/json'}
                response = requests.post(path, json_data, headers=headers, auth=(username, password))
            elif method == 'PUT':
                json_data = json_dumps(data or {})
                headers   = {'Content-Type': 'application/json'}
                response = requests.put(path, json_data, headers=headers, auth=(username, password))
            elif method == 'DELETE':
                response = requests.delete(path, auth=(username, password))
            else:
                log_error(f'[Error][request_method]: unsupported method {method} for path: {path}')
                return None
        else:
            response = requests.get(path)
        if response.status_code >= 404:
            log_error(f'[Error][request_get][404] for path {path}: {response.text}')
            return response.text
        if response.status_code >= 200 or response.status_code < 300:
            if 'image/' in response.headers.get('content-type'):
                return response.content
            if response.headers.get('Content-Type') == 'application/json;charset=UTF-8':
                if response.text == '':
                    return {}
                return response.json()
            return response.text
        else:
            log_error(f'[Error][request_get] for path {path}: {response.text}')
        return None

    def request_post(self,path, data):
        return self.request_method('POST', path=path, data=data)

    def request_put(self, path, put_data):
        return self.request_method('PUT', path=path, data=put_data)

        # json_data = json_dumps(data)
        # (server, username, password) = self.config()
        # path = '{0}/rest/api/2/{1}'.format(server, path)
        # if self.log_requests: Dev.pprint('put', path)
        # headers = {'Content-Type': 'application/json'}
        # response = requests.put(path, json_data, headers=headers, auth=(username, password))
        # if 200 <= response.status_code < 300:
        #     return True
        # Dev.pprint('[Error][request_put]: {0}'.format(response.text))
        # return False

    # methods

    @index_by
    def fields(self):
        if self._fields is None:
            self._fields =  self.request_get('field')
        return self._fields

    @cache_on_self
    def fields_by_id(self):
        fields = {}
        for field in self.fields():
            fields[field.get('id')] = field
        return fields

    def fields_by_name(self):                                       #need to add local temp cache for this (since this is quite an expensive call
        fields = {}
        for field in self.fields():
            fields[field.get('name')] = field
        return fields

    def issue_add_link(self, source_id, target_id, link_type):
        path = f'issue/{source_id}'
        put_data = {"update":{ "issuelinks":[ { "add":{ "type":{
                                                        "name":link_type,
                                                        },
                                                "outwardIssue":{ "key":target_id }}}]}}
        return self.request_put(path=path, put_data=put_data)

    def issue_delete(self, issue_id):
        if issue_id:
            path = f'issue/{issue_id}'
            return self.request_delete(path)

    def issue_raw(self,issue_id,fields='*all'):
        if issue_id:
            path = 'issue/{0}?fields={1}'.format(issue_id,fields)
            return self.request_get(path)

    def map_issue_links(self, issue, issue_links_raw):
        issue_links = {}
        if issue_links_raw:
            for item in issue_links_raw:
                if item.get('outwardIssue'):
                    link_key  = item.get('outwardIssue').get('key')
                    link_type = item.get('type').get('outward')
                else:
                    link_key  = item.get('inwardIssue').get('key')
                    link_type = item.get('type').get('inward')
                if issue_links.get(link_type) is None:
                    issue_links[link_type] = []
                issue_links[link_type].append(link_key)

        issue['Issue Links'] = issue_links                  # todo: see what is the side effect of not including this by default
        return self

    def convert_issue(self, issue_raw):
        if issue_raw:
            skip_fields    = [ 'issuerestriction','resolution', 'votes','worklog','watches','comment',
                              'iconUrl','fixVersions', 'customfield_14238',
                              'issuelinks', 'timetracking'] # '% complete'
            skip_types       = ['any','progress','option-with-child']
            use_display_name = ['user']
            use_name         = ['issuetype','status','project','priority', 'securitylevel']
            use_value        = ['string', 'number','datetime', 'date','issuerestriction']
            if issue_raw:

                issue_key = issue_raw['key']
                #issue_id  = issue_raw['id']
                #issue    = { 'Key' : issue_key , 'Id': issue_id }
                issue    = { 'Key' : issue_key }                    # todo: see what is the side effects of not including the Jira internal issue ID (which is not really used anywhere)
                fields   = self.fields_by_id()
                fields_values = issue_raw.get('fields') or {}
                self.map_issue_links(issue, fields_values.get('issuelinks'))
                if fields_values:
                    for field_id,value in fields_values.items():
                        if value and field_id not in skip_fields:
                            if field_id == 'parent':
                                issue['Parent'] = fields_values.get('parent').get('key')
                                continue
                            field = fields.get(field_id)

                            issue_type = field.get('schema').get('type')

                            if issue_type not in skip_types:
                                issue_name = field.get('name')
                                if issue_type in use_display_name: value = value.get('displayName')
                                elif issue_type in use_name      : value = value.get('name')
                                elif issue_type in use_value     : value = value
                                elif issue_type == 'option'      : value = value.get('value')
                                elif issue_type == 'array'       :
                                    items = []
                                    for item in value:
                                        if type(item) is str: items.append(item)
                                        else:
                                            if item.get('value'):
                                                items.append(item.get('value'))
                                            elif item.get('name'):
                                                items.append(item.get('name'))
                                    value = ",".join(items)
                                else:
                                    print(">> in convert_issue")
                                    print('>> ', field_id,issue_type)
                                    Dev.pprint(value)
                                    continue
                                issue[issue_name] = value
                return issue
        return {}


    def issue(self,issue_id,fields='*all'):
        issue_raw = self.issue_raw(issue_id,fields)
        if type(issue_raw) is str: # happens  ["Issue does not exist or you do not have permission to see it."]:
            return {}
        return self.convert_issue(issue_raw)

    def issues(self,issues_ids,fields=None):
        chunk_size = 100                            # split the # of issues to fetch (to handle request_get and jira limitations (that happened when trying to fetch more than 250 issues
        issues = {}
        if fields is None:
            fields = '*all'

        for chuck in list_chunks(list=issues_ids,split_by=chunk_size):
            jql = f"key in {chuck}".replace('[', '(').replace(']', ')')
            result = self.search(jql=jql, fields=fields)
            for issue in result:
                key = issue.get('Key')
                issues[key] = issue
        return issues

        #for issue_id in issues_ids:
        #    issue = self.issue(issue_id,fields)
        #    if issue:
        #        issues[issue_id] = issue
        #return issues

    def issue_create(self, project, issue_type, summary, description=None, extra_fields=None):
        path     = 'issue'
        fields   = {  "project"    : { "key": project }   ,
                      "summary"    : summary              ,
                      "description": description          ,
                      "issuetype"  : { "name": issue_type }}
        post_data = { "fields": fields | (extra_fields or {})}

        # if extra_fields:
        #     post_data.get('fields', {}).extend(extra_fields)
        return self.request_post(path, post_data)
        return post_data

    def issue_update_field(self, issue_id, field,value):
        return self.issue_update_fields(issue_id, {field:value})

    def issue_update_fields(self, issue_id, fields):
        path = 'issue/{0}'.format(issue_id)
        data = { "update" : {}}
        fields_by_name = self.fields_by_name()
        for key,value in fields.items():
            if key == 'Rating': key = 'Risk Rating'     # move to special resolver method (needed because 'Risk Rating' was mapped as 'Rating' in ELK)
            field = fields_by_name.get(key)
            if field:
                field_id    = field.get('id')
                schema_type = field.get('schema').get('type')
                #print(field_id, schema_type)
                if   schema_type == 'option'   : data['update'][field_id] =[{"set": {'value': value }}]
                elif schema_type == 'string'   : data['update'][field_id] = [{"set": value}]
                elif schema_type == 'array'    : data['update'][field_id] = [{"set": value.split(',')}]
                elif schema_type == 'user'     : data['update'][field_id] = [{"set": {'name': value }}]
                else                           : data['update'][field_id] = [{"set": value}]

                #Dev.pprint(field)issue_update
        if len(set(data)) == 0:
            return False
            #Dev.pprint(data)
        return self.request_put(path, data) is not None

    def issue_status_available(self, issue_id):
        items = {}
        if issue_id:
            path = 'issue/{0}/transitions'.format(issue_id)
            data = self.request_get(path)
            if data:
                for transition in data.get('transitions'):
                    to_data = transition.get('to')
                    items[to_data.get('name')] = to_data.get('id')
        return items

    def projects(self):
        projects = {}
        #data = self.request_get('issue/createmeta').get('projects')
        data = self.request_get('project')
        for item in data:
            projects[item.get('key')] = item
        return projects

    def projects_icons(self):
        icons = {}
        for key,project in self.projects().items():
            icons[key] = project.get('avatarUrls').get('48x48')
        return icons

    @index_by
    def search(self, jql='', fetch_all=True, fields='*all', start_at=0, max_to_fetch=-1):
        if -1 < max_to_fetch < 100:                 # todo improve logic of max_to_fetch since at the moment it will fetch 300 for values of 200, 210,250, 290
            max_results = max_to_fetch              # in case the max_to_fetch is between 0 and 100 (this part is working)
        else:
            max_results = 100                       # 100 seems to be the current limit of Jira cloud
        results = []
        start_at = start_at
        while True:
            path  = f'search?jql={jql}&startAt={start_at}&maxResults={max_results}&fields={fields}'

            data  = self.request_get(path)
            if data is None:
                return results
            if data:
                issues = data.get('issues', [])
                for issue in issues:
                    results.append(self.convert_issue(issue))
                if len(results) == data.get('total'):
                    break
                if -1 < max_to_fetch <= len(results):
                    break
                if fetch_all is False:
                    break
                if len(issues) == 0:
                    break
                start_at += len(issues)
            else:
                break
        return results

    def search__return_keys(self, jql):
        result = self.search(jql=jql, fields = 'key', index_by='Key')
        return list_set(result)

    def webhook_failed(self):
        return self.request_get('webhook/failed')