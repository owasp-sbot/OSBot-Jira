import json

from gw_bot.helpers.Lambda_Helpers import log_to_elk
from gw_bot.lambdas.png_to_slack   import load_dependencies

def api_jira_rest():
    from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
    return API_Jira_Rest()

def elastic():
    secrets_id = 'gw-elastic-server-1'
    index_id = 'jira'
    from gw_bot.elastic.Elastic_Search import Elastic_Search
    return Elastic_Search(index_id, secrets_id)

def add_to_elk(issue):
    elastic().add(issue,'Key')

def get_jira_issue(issue_id_or_key):
    return api_jira_rest().issue(issue_id_or_key)

def handle_issuelink_created(data):
    return 'issuelink_created'

def handle_link_change(data):
    issue_link        = data.get('issueLink')
    event_type        = data.get('webhookEvent')
    source            = issue_link.get('sourceIssueId')
    destination       = issue_link.get('destinationIssueId')
    link_type         = issue_link.get('issueLinkType').get('name')
    issue_source      = get_jira_issue(source)
    issue_destination = get_jira_issue(destination)
    add_to_elk(issue_source)
    add_to_elk(issue_destination)
    return f"'{link_type}' {event_type} from '{issue_source.get('Key')}' to {issue_destination.get('Key')}'"

def handle_link_deleted(data):
    user = data.get('user').get('displayName')
    key  = data.get('issue').get('key')
    result = api_jira_rest().issue_delete(key)
    return f"the user '{user}' | deleted the issue '{key}' : {result}"

def run(event, context):
    load_dependencies('requests,elastic')
    data = json.loads(event.get('body'))
    try:
        event_type = data.get('webhookEvent')
        if event_type == 'issuelink_deleted':               # link deleted
            message = handle_link_change(data)
        #elif event_type == 'issuelink_created':            # link created
        #    message = handle_link_change(data)
        elif event_type == 'jira:issue_deleted':            # issue deleted
            message = handle_link_deleted(data)
        elif event_type == 'jira:issue_updated':            # issue updated
            user = data.get('user').get('displayName')
            issue_raw  = data.get('issue')
            change_log = data.get('changelog')
            key         = issue_raw.get('key')
            issue   = api_jira_rest().convert_issue(issue_raw)
            add_to_elk(issue)
            data    = issue
            message = f"the user '{user}' | updated the issue '{key}' | after event '{event_type}'  | \n change log: {change_log}"
        else:
            message = f"unsuported event_type: {event_type}"
            data    = event.get('body')

        log_to_elk(message, data, index='elastic_logs')
    except Exception as error:
        error_message = f'error in on_jira_change: {error}'
        log_to_elk(error_message, data, index='elastic_logs', level='error')
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "headers": {},
            "body": error_message
        }

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": message
    }