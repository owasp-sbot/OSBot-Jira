import requests
from dotenv import load_dotenv
from osbot_utils.decorators.lists.index_by        import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from osbot_utils.testing.Duration   import Duration
from osbot_utils.utils.Dev          import Dev
from osbot_utils.utils.Files        import path_combine, create_folder, file_create_bytes, file_not_exists
from osbot_utils.utils.Json         import json_dumps, file_create_json
from osbot_utils.utils.Lists        import list_chunks
from osbot_utils.utils.Misc         import  list_set, date_time_now_less_time_delta, upper
from osbot_utils.utils.Objects import env_vars


class API_Jira_Rest:

    def __init__(self):
        self.secrets_id          = 'GS_BOT_GS_JIRA'
        self.jira_env_vars       = {'JIRA_API_EMAIL', 'JIRA_API_TOKEN', 'JIRA_API_SERVER'}
        self._config             = None
        self._fields             = None               # cache this value per request (since it is expensive and data doesn't change that much)
        self.log_requests        = False
        self.allow_requests      = True

    def config(self):
        if self._config is None:
            load_dotenv()
            if set(self.jira_env_vars).issubset(set(env_vars())):
                self._config = self.config_using_env_vars()
            else:
                self._config = self.config_using_aws_secrets()

        return self._config

    def config_using_aws_secrets(self):
        from osbot_aws.apis.Secrets import Secrets                                  # todo: refactor this out of this class (so that we don't have a dependency in AWS
        data = Secrets(self.secrets_id).value_from_json_string() or {}
        return (data.get('server'), data.get('username'), data.get('password'))


    def config_using_env_vars(self):
        vars     = env_vars()
        username = vars.get('JIRA_API_EMAIL')
        password = vars.get('JIRA_API_TOKEN')
        server   = vars.get('JIRA_API_SERVER')
        return (server, username, password)

    def disable_requests(self):
        self.allow_requests = False
        return self

    def set_public_jira(self, server):
        self._config = (server, "", "")
        return self

    def set_log_requests(self, value=True):
        self.log_requests = value
        return self

    # request helpers

    def request_target(self, path):
        (server, username, password) = self.config()
        if server is None:
            return None
        if path.startswith('http') is False:
            if server.endswith('/') is False:
                server += '/'
            path = '{0}rest/api/2/{1}'.format(server, path)
        target = path
        return (target, username, password)

    def request_get_redirect(self, path):
        (target, username, password) = self.request_target(path)
        #print(target)
        response  = requests.get(target, auth=(username, password),allow_redirects=False)
        return response.text
        #return response.headers.get('Location')

    def request_get(self,path,always_return_content=False):
        return self.request_method('GET', path, always_return_content=always_return_content)

    def request_delete(self,path):
        return self.request_method('DELETE', path)

    def request_method(self,method, path, data=None, always_return_content=False):
        if self.allow_requests is False:
            return None
        (target, username, password) = self.request_target(path)
        if self.log_requests:
            print('jira_rest_api_path:',method, target)
        if username and password:
            if method =='GET':
                response = requests.get(target, auth=(username, password))
            elif method == 'POST':
                json_data = json_dumps(data or {})
                headers   = {'Content-Type': 'application/json'}
                response = requests.post(target, json_data, headers=headers, auth=(username, password))
            elif method == 'PUT':
                json_data = json_dumps(data or {})
                headers   = {'Content-Type': 'application/json'}
                response = requests.put(target, json_data, headers=headers, auth=(username, password))
            elif method == 'DELETE':
                response = requests.delete(target, auth=(username, password))
            else:
                print(f'[Error][request_method]: unsupported method {method} for target: {target}')
                return None
        else:
            response = requests.get(target)
        if response.status_code >= 400:
            print(f'[Error][request_get][404] for target {target}: {response.text}')
            return response.text
        if response.status_code >= 200 or response.status_code < 300:
            if always_return_content:
                return response.content
            if 'image/' in response.headers.get('content-type'):
                return response.content
            if response.headers.get('Content-Type') == 'application/json;charset=UTF-8':
                if response.text == '':
                    return {}
                return response.json()
            return response.text
        else:
            print(f'[Error][request_get] for target {target}: {response.text}')
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

    def issue_attachment_download(self, attachment_id):
        path = f'attachment/content/{attachment_id}'
        return self.request_get(path, always_return_content=True)

    def issue_attachment_thumbnail_download(self, attachment_id):
        path = f'attachment/thumbnail/{attachment_id}'
        return self.request_get(path, always_return_content=True)

    def issue_attachments(self, issue_id):
        result = []
        attachments = self.issue(issue_id).get('Attachments', [])
        for attachment in attachments:
            attachment_id      = attachment.get('id')
            attachment_content = self.issue_attachment_download(attachment_id=attachment_id)
            result.append({'metadata': attachment, 'content': len(attachment_content)})
            break
        return result

    def issue_delete(self, issue_id):
        if issue_id:
            path = f'issue/{issue_id}'
            return self.request_delete(path)

    def issue_delete_link(self, link_id):
        if link_id:
            path = f'issueLink/{link_id}'
            if self.request_delete(path) == {}:
                return True
        return False

    def issue_download_to_folder(self, issue_id, target_folder, download_thumbnails=False):
        folder_issue       = path_combine(target_folder, issue_id         )
        file_issue         = path_combine(folder_issue , f'issue.json'    )
        file_issue_raw     = path_combine(folder_issue , f'issue_raw.json')
        file_attachments   = []
        create_folder(folder_issue)

        issue_raw_data   = self.issue_raw(issue_id)
        if type(issue_raw_data) is str:                     # happens when  ["Issue does not exist or you do not have permission to see it."]:
            issue_data = {}
        else:
            issue_data = self.convert_issue(issue_raw_data)


        file_create_json(python_object=issue_data    , path=file_issue)
        file_create_json(python_object=issue_raw_data, path=file_issue_raw)
        for attachment in issue_data.get('Attachments', []):
            attachment_id   = attachment.get('id')
            file_attachment = path_combine(folder_issue, attachment_id)
            if file_not_exists(file_attachment):
                attachment_data = self.issue_attachment_download(attachment_id)
                file_create_bytes(bytes=attachment_data, path=file_attachment)
            file_attachments.append(file_attachment)
            if download_thumbnails:
                file_thumbnail_attachment = path_combine(folder_issue, f'{attachment_id}_thumbnail.png')  # todo: this extension is not 100% since I've seen jpegs here (but at the moment the issue_attachment_thumbnail_download just returns the data and no clue of what the thumbnail file type is)
                if file_not_exists(file_thumbnail_attachment):
                    attachment_thumbnail_data = self.issue_attachment_thumbnail_download(attachment_id)
                    file_create_bytes(bytes=attachment_thumbnail_data, path=file_thumbnail_attachment)


        return {'folder_issue'     : folder_issue     ,
                'file_issue'       : file_issue       ,
                'file_issue_raw'   : file_issue_raw   ,
                'file_attachments' : file_attachments }

    def issue_links_ids(self, source_id):
        links_ids = {}
        path     = f'issue/{source_id}?fields=issuelinks'
        raw_data = self.request_get(path)
        issues_links = raw_data.get('fields', {}).get('issuelinks', [])
        for issue_link in issues_links:
            link_id   = issue_link.get('id')
            if issue_link.get('outwardIssue'):
                target_id =  issue_link.get('outwardIssue', {}).get('key')
                link_type =  issue_link.get('type', {}).get('outward')
            else:
                target_id = issue_link.get('inwardIssue', {}).get('key')
                link_type = issue_link.get('type', {}).get('inward')
            #pprint(issues_links)
            edge = (source_id, link_type,target_id)
            links_ids[edge] = link_id
        return links_ids


    def issue_link_id(self, source_id, target_id, link_type):
        links_ids = self.issue_links_ids(source_id=source_id)
        edge     = (source_id, link_type, target_id)
        return links_ids.get(edge)

    def issue_raw(self,issue_id,fields='*all'):
        if issue_id:
            path = 'issue/{0}?fields={1}'.format(upper(str(issue_id)),fields)
            return self.request_get(path)

    def map_issue_links(self, issue, issue_links_raw, expand_issue_links=False):
        issue_links = {}
        if issue_links_raw:
            for item in issue_links_raw:
                if item.get('outwardIssue'):
                    fields    = item.get('outwardIssue').get('fields')
                    link_key  = item.get('outwardIssue').get('key')
                    link_type = item.get('type').get('outward')
                else:
                    fields    = item.get('inwardIssue').get('fields')
                    link_key  = item.get('inwardIssue').get('key')
                    link_type = item.get('type').get('inward')
                if expand_issue_links:
                    issue_type = fields.get('issuetype').get('name')
                    priority   = fields.get('priority').get('name')
                    status     = fields.get('status').get('name')
                    summary    = fields.get('summary')
                    link_data  = {'Key'       : link_key   ,
                                  'Issue Type': issue_type ,
                                  'Priority'  : priority   ,
                                  'Status'    : status     ,
                                  'Summary'   : summary    }
                    if issue_links.get(link_type) is None:
                        issue_links[link_type] = {}
                    issue_links[link_type][link_key] = link_data
                else:
                    if issue_links.get(link_type) is None:
                        issue_links[link_type] = []
                    issue_links[link_type].append(link_key)

        issue['Issue Links'] = issue_links                  # todo: see what is the side effect of not including this by default
        return self

    def convert_attachments(self, data):
        attachments = []
        if type(data) is list:
            for item in data:
                attachment = {"created": item.get('created' ),
                              "name"   : item.get('filename'),
                              "id"     : item.get('id'      ),
                              "type"   : item.get('mimeType'),
                              "size"   : item.get('size'    )}
                attachments.append(attachment)
        return attachments

    def convert_issue(self, issue_raw, expand_issue_links=False):
        if issue_raw:
            skip_fields    = [ 'workratio','lastViewed','issuerestriction','resolution', 'votes','worklog','watches','comment',
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
                self.map_issue_links(issue, fields_values.get('issuelinks'), expand_issue_links=expand_issue_links)
                if fields_values:
                    for field_id,value in fields_values.items():
                        if value and field_id not in skip_fields:
                            if field_id == 'parent':
                                issue['Parent'] = fields_values.get('parent').get('key')
                                continue
                            if field_id == 'attachment':
                                issue['Attachments'] = self.convert_attachments(value)
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
                                #print(issue_name,field_id)
                                issue[issue_name] = value
                return issue
        return {}


    def issue(self,issue_id,fields='*all', expand_issue_links=False):
        issue_raw = self.issue_raw(issue_id,fields)
        if type(issue_raw) is str: # happens  ["Issue does not exist or you do not have permission to see it."]:
            return {}
        return self.convert_issue(issue_raw,expand_issue_links=expand_issue_links)

    def issues(self,issues_ids,fields=None):
        with Duration(prefix="Fetch issues", print_result=False):
            chunk_size = 100                            # split the # of issues to fetch (to handle request_get and jira limitations (that happened when trying to fetch more than 250 issues
            issues = {}
            if fields is None:
                fields = '*all'

            for chuck in list_chunks(items=issues_ids,split=chunk_size):
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

    # this is fast because (in a Jira Cloud with 6k issues) it will execute in one request
    #@cache_on_tmp()
    def issues_get_all_ids(self):
        return self.search__return_keys(jql="ORDER BY created DESC")

    def issue_create(self, project, issue_type, summary, description=None, extra_fields=None):
        path     = 'issue'
        fields   = {  "project"    : { "key": project }   ,
                      "summary"    : summary              ,
                      "description": description          ,
                      "issuetype"  : { "name": issue_type }}
        post_data = { "fields": fields | (extra_fields or {})}

        return self.request_post(path, post_data)

    def issue_update_field(self, issue_id, field,value):
        return self.issue_update_fields(issue_id, {field:value})

    def issue_update_fields(self, issue_id, fields):
        path = 'issue/{0}'.format(issue_id)
        data = { "update" : {}}
        fields_by_name = self.fields_by_name()
        for key,value in fields.items():
            #if key == 'Rating': key = 'Risk Rating'     # move to special resolver method (needed because 'Risk Rating' was mapped as 'Rating' in ELK)
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
    def search(self, jql, fetch_all=True, fields='*all', start_at=0, max_to_fetch=-1, expand_issue_links=False):
        if jql == '':
            return []                                                                                # don't allow empty queries since this is most likely a mistake (and the way this method is designed it will fetch all data from Jira)
        if -1 < max_to_fetch:                                                                        # If max_to_fetch is within 0 and 100, sets max_results to max_to_fetch, limiting the fetched issues to that number. todo: ensure logic correctly handles numbers close to 300, e.g. 210, 250, 290.
            max_results = max_to_fetch                                                               # Defines the max_results to limit the number of fetched results.
        else:
            max_results = -1                                                                         # Sets max_results to -1 to handle varying number of fields. If fewer fields like 'key' are specified, Jira returns all values in one request, otherwise, it batches them in 100.
        results = []
        start_at = start_at                                                                          # Initializes start_at for pagination.
        while True:                                                                                  # Initiates loop to continuously fetch issues until conditions to break are met.
            path  = f'search?jql={jql}&startAt={start_at}&maxResults={max_results}&fields={fields}'  # Constructs the API path with query parameters.
            data  = self.request_get(path)                                                           # Calls the request_get method to get the data from Jira.
            if data is None or type(data) is str:                                                    # If the received data is None or a string, returns the results list, which may be empty.
                return results
            if data:                                                                                 # If there is valid data received:
                issues = data.get('issues', [])                                                      # Extracts issues from the data, defaults to an empty list if 'issues' key is not present.
                for issue in issues:                                                                 # Iterates over each issue.
                    results.append(self.convert_issue(issue, expand_issue_links=expand_issue_links)) # Converts and appends each issue to the results list.
                if len(results) == data.get('total'):                                                # If the length of results is equal to the total number of issues, breaks the loop.
                    break
                if -1 < max_to_fetch <= len(results):                                                # If max_to_fetch is defined and the length of results has reached this number, breaks the loop.
                    break
                if fetch_all is False:                                                               # If fetch_all is False, breaks the loop after the first batch of issues.
                    break
                if len(issues) == 0:                                                                 # If there are no more issues left to fetch, breaks the loop.
                    break
                start_at += len(issues)                                                              # Increments start_at by the number of issues fetched in the last request for pagination.
            else:
                break                                                                                # Breaks the loop if no data is received.
        return results                                                                               # Returns the list of fetched and converted issues.


    def search_updated_since(self, days=0, hours=0, minutes=0):
        query_date = date_time_now_less_time_delta(days=days, hours=hours, minutes=minutes, date_time_format='%Y-%m-%d %H:%M')
        return self.search_updated_since(query_date)

    def search_updated_since_query_date(self, query_date):
        jql = f'updated >= "{query_date}"'
        return self.search(jql=jql)

    def search__return_keys(self, jql, max_to_fetch=-1):
        result = self.search(jql=jql, fields = 'key', index_by='Key', max_to_fetch=max_to_fetch)
        return list_set(result)

    def webhook_failed(self):
        return self.request_get('webhook/failed')