from functools import lru_cache

from osbot_aws.helpers.Lambda_Helpers import log_to_elk
from osbot_elastic.Elastic_Search import Elastic_Search

from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest

class API_Jira_To_Elastic:

    def __init__(self):
        self.secrets_id = 'gw-elastic-server-1'
        self.index_id   = 'jira'

    @lru_cache(maxsize=None)
    def api_jira_rest(self):
        return API_Jira_Rest()

    @lru_cache(maxsize=None)
    def elastic(self):
        return Elastic_Search(self.index_id, self.secrets_id)

    # handle methods

    def handle_event(self,event_type, user_id, data):
        log_message = 'API_Jira_To_Elastic.handle_event'
        if event_type   == 'issuelink_deleted':                            # link deleted
            log_data     = self.handle_link_event(data, 'link_deleted')
        elif event_type == 'issuelink_created':                            # link created
            log_data     = self.handle_link_event(data, 'link_created')
        elif event_type == 'jira:issue_created':
            log_data     = self.handle_issue_created(data)
        elif event_type == 'jira:issue_deleted':                           # issue deleted
            log_data     = self.handle_issue_deleted(data)
        elif event_type == 'jira:issue_updated':                           # issue updated
            log_data     = self.handle_issue_updated(data)
        else:
            log_data     = { 'event_type'     : f'unsupported event_type: {event_type}',
                             'event_user'     : 'NA'                                   ,
                             'event_key'      : 'NA'                                   ,
                             'raw_data'       : f'{data}'                              }

        log_data['user_id'] = user_id


        return log_to_elk(log_message, log_data, index='elastic_logs')

    def handle_issue_updated(self,data):
        user         = data.get('user').get('displayName')
        issue_raw    = data.get('issue')
        change_log   = data.get('changelog')
        key          = issue_raw.get('key')
        issue        = self.api_jira_rest().convert_issue(issue_raw)
        self.add_to_elk(issue)
        log_data     = { 'event_type'     : 'issue_updated',
                         'event_user'     : user           ,        # just user was conflicting with user object already on Elastic
                         'event_key'      : key            ,
                         'change_log'     : change_log
                       }
        return log_data

    def handle_issue_created(self, data):
        user      = data.get('user').get('displayName')
        issue_raw = data.get('issue')
        key       = issue_raw.get('key')
        issue     = self.api_jira_rest().convert_issue(issue_raw)
        self.add_to_elk(issue)
        return { 'event_type': 'issue_created',
                 'event_user': user,
                 'event_key' : key,
                 'issue'     : issue}

    def handle_issue_deleted(self, data):
        user = data.get('user').get('displayName')
        issue_raw = data.get('issue')
        key       = issue_raw.get('key')
        issue     = self.api_jira_rest().convert_issue(issue_raw)
        log_data = {'event_type': 'issue_deleted',
                    'event_user': user,
                    'event_key' : key,
                    'issue'     : issue}
        self.elastic().delete_data_by_id(key)
        return log_data

    def handle_link_event(self, data, event_type):
        issue_link        = data.get      ('issueLink'         , {})
        source            = issue_link.get('sourceIssueId'     , {})
        destination       = issue_link.get('destinationIssueId', {})
        link_type         = issue_link.get('issueLinkType'     , {}).get('name')
        issue_source      = self.get_jira_issue(source)
        issue_destination = self.get_jira_issue(destination)
        self.add_to_elk(issue_source)
        self.add_to_elk(issue_destination)
        return  {'event_type': event_type,
                 'event_user': 'NA',
                 'event_key' : f'{issue_source.get("Key")} {link_type} {issue_destination.get("Key")}',
                 'raw_data'  : data }

    # main methods
    def add_to_elk(self, issue):
        return self.elastic().add(issue, 'Key')

    def get_jira_issue(self, issue_id_or_key):
        return self.api_jira_rest().issue(issue_id_or_key)






