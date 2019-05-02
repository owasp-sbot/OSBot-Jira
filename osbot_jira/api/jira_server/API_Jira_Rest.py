import requests
from osbot_aws.apis.Secrets import Secrets

from pbx_gs_python_utils.utils.Dev import Dev
#from pbx_gs_python_utils.utils.Local_Cache import use_local_cache_if_available
from pbx_gs_python_utils.utils.Misc import Misc


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

    def request_get(self,path):
        (server, username, password)= self.config()
        path = '{0}/rest/api/2/{1}'.format(server, path)
        if self.log_requests: Dev.pprint('get', path)
        response = requests.get(path, auth=(username, password))
        if response.status_code == 200:
            return response.text
        Dev.pprint('[Error][request_get]: {0}'.format(response.text))
        return None

    def request_put(self, path, data):
        json_data = Misc.json_dumps(data)
        (server, username, password) = self.config()
        path = '{0}/rest/api/2/{1}'.format(server, path)
        if self.log_requests: Dev.pprint('put', path)
        headers = {'Content-Type': 'application/json'}
        response = requests.put(path, json_data, headers=headers, auth=(username, password))
        if 200 <= response.status_code < 300:
            return True
        Dev.pprint('[Error][request_put]: {0}'.format(response.text))
        return False

    def fields(self):
        if self._fields is None:
            self._fields =  Misc.json_load(self.request_get('field'))
        return self._fields

    #@use_local_cache_if_available
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

    #@use_local_cache_if_available
    def issue_raw(self,issue_id,fields='*all'):
        if issue_id:
            path = 'issue/{0}?fields={1}'.format(issue_id,fields)
            data = self.request_get(path)
            return Misc.json_load(data)

    def issue(self,issue_id,fields='*all'):
        issue_raw = self.issue_raw(issue_id,fields)
        if issue_raw:
            skip_fields    = ['resolution', 'votes','worklog','watches','comment',
                              'iconUrl','fixVersions', 'customfield_14238',
                              'issuelinks'] # '% complete'
            skip_types     = ['any','progress','option-with-child']
            use_name_value = ['user', 'issuetype','status','project','priority', 'securitylevel']
            use_value      = ['string', 'number','datetime', 'date']
            if issue_raw:
                issue  = {'Key' : issue_id}
                fields = self.fields_by_id()
                fields_values = issue_raw.get('fields')
                if fields_values:
                    for field_id,value in fields_values.items():
                        if value and field_id not in skip_fields:
                            field = fields.get(field_id)
                            issue_type = field.get('schema').get('type')
                            if issue_type not in skip_types:
                                issue_name = field.get('name')
                                #Dev.pprint(fields.get(field_id))

                                if issue_type in use_name_value : value = value.get('name')
                                elif issue_type in use_value    : value = value
                                elif issue_type == 'option'     : value = value.get('value')
                                elif issue_type == 'array'      :
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
                                    print('>> ', field_id,issue_type)
                                    Dev.pprint(value)
                                    continue
                                issue[issue_name] = value


                return issue

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
                for transition in Misc.json_load(data).get('transitions'):
                    to_data = transition.get('to')
                    items[to_data.get('name')] = to_data.get('id')
        return items