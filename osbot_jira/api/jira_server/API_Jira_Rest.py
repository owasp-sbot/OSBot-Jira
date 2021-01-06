import json

import requests

from osbot_aws.helpers.Lambda_Helpers import log_error
from osbot_aws.apis.Secrets import Secrets
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Json import json_dumps, json_loads


class API_Jira_Rest:
    def __init__(self):
        self.secrets_id = 'GS_BOT_GS_JIRA'
        self._config      = None
        self._fields      = None               # cache this value per request (since it is expensive and data doesn't change that much)
        self.log_requests = False

    def config(self):
        if self._config is None:
            data = Secrets(self.secrets_id).value_from_json_string()
            self._config = (data.get('server'), data.get('username'), data.get('password'))
        return self._config

    def set_public_jira(self, server):
        self._config = (server, "", "")
        return self

    # request helpers

    def request_get(self,path):
        return self.request_method('GET', path)

    def request_delete(self,path):
        return self.request_method('DELETE', path)

    def request_method(self,method, path):
        (server, username, password)= self.config()
        if path.startswith('http') is False:
            path = '{0}/rest/api/2/{1}'.format(server, path)
        if self.log_requests: Dev.pprint('get', path)
        if username and password:
            if method =='GET':
                response = requests.get(path, auth=(username, password))
            elif method == 'DELETE':
                response = requests.delete(path, auth=(username, password))
            else:
                log_error(f'[Error][request_method]: unsupported method {method} for path: {path}')
                return None
        else:
            response = requests.get(path)
        if response.status_code == 200:
            if 'image/' in response.headers.get('content-type'):
                return response.content
            return response.text
        else:
            log_error(f'[Error][request_get] for path {path}: {response.text}')
        return None

    def request_put(self, path, data):
        json_data = json_dumps(data)
        (server, username, password) = self.config()
        path = '{0}/rest/api/2/{1}'.format(server, path)
        if self.log_requests: Dev.pprint('put', path)
        headers = {'Content-Type': 'application/json'}
        response = requests.put(path, json_data, headers=headers, auth=(username, password))
        if 200 <= response.status_code < 300:
            return True
        Dev.pprint('[Error][request_put]: {0}'.format(response.text))
        return False

    # methods

    @index_by
    def fields(self):
        if self._fields is None:
            self._fields =  json_loads(self.request_get('field'))
        return self._fields

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

    def issue_delete(self, issue_id):
        if issue_id:
            path = f'issue/{issue_id}'
            data = self.request_delete(path)
            return json_loads(data)

    def issue_raw(self,issue_id,fields='*all'):
        if issue_id:
            path = 'issue/{0}?fields={1}'.format(issue_id,fields)
            data = self.request_get(path)
            return json_loads(data)

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

        issue['Issue Links'] = issue_links
        return self

    def convert_issue(self, issue_raw):
        if issue_raw:
            skip_fields    = ['resolution', 'votes','worklog','watches','comment',
                              'iconUrl','fixVersions', 'customfield_14238',
                              'issuelinks'] # '% complete'
            skip_types       = ['any','progress','option-with-child']
            use_display_name = ['user']
            use_name         = ['issuetype','status','project','priority', 'securitylevel']
            use_value        = ['string', 'number','datetime', 'date']
            if issue_raw:

                issue_key = issue_raw['key']
                issue_id  = issue_raw['id']
                issue    = { 'Key' : issue_key , 'Id': issue_id }
                fields   = self.fields_by_id()
                fields_values = issue_raw.get('fields')
                self.map_issue_links(issue, fields_values.get('issuelinks'))
                if fields_values:
                    for field_id,value in fields_values.items():
                        if value and field_id not in skip_fields:
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
                                    #print('>> ', field_id,issue_type)
                                    Dev.pprint(value)
                                    continue
                                issue[issue_name] = value


                return issue
        return {}


    def issue(self,issue_id,fields='*all'):
        issue_raw = self.issue_raw(issue_id,fields)
        return self.convert_issue(issue_raw)


    def issues(self,issues_ids,fields='*all'):
        issues = {}
        for issue_id in issues_ids:
            issue = self.issue(issue_id,fields)
            if issue:
                issues[issue_id] = issue
        return issues

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
        return self.request_put(path, data)

    def issue_status_available(self, issue_id):
        items = {}
        if issue_id:
            path = 'issue/{0}/transitions'.format(issue_id)
            data = self.request_get(path)
            if data:
                for transition in json_loads(data).get('transitions'):
                    to_data = transition.get('to')
                    items[to_data.get('name')] = to_data.get('id')
        return items

    def projects(self):
        projects = {}
        data = json_loads(self.request_get('issue/createmeta')).get('projects')
        for item in data:
            projects[item.get('key')] = item
        return projects

    def projects_icons(self):
        icons = {}
        for key,project in self.projects().items():
            icons[key] = project.get('avatarUrls').get('48x48')
        return icons

    def search(self, jql='', fetch_all=True):
        max_results = 100  # 100 seems to be the current limit of Jira cloud
        results = []
        start_at = 0
        while True:
            path  = f'search?jql={jql}&startAt={start_at}&maxResults={max_results}'
            if self.request_get(path) is None:
                return results
            data  = json.loads(self.request_get(path))
            issues = data['issues']
            for issue in issues:
                results.append(self.convert_issue(issue))
            if fetch_all is False:
                break
            if len(issues) == 0:
                break
            start_at += len(issues)

        return results

    def webhook_failed(self):
        return self.request_get('webhook/failed')