import json

from gw_bot.helpers.Lambda_Helpers import log_to_elk
from osbot_aws.Dependencies import load_dependencies


def run(event, context):
    load_dependencies('requests,elastic')
    from osbot_jira.api.jira_server.API_Jira_To_Elastic import API_Jira_To_Elastic
    try:
        data       = json.loads(event.get('body'))
        event_type = data.get('webhookEvent')
        user_id    = event.get('queryStringParameters').get('user_id')
        message = API_Jira_To_Elastic().handle_event(event_type, user_id, data)
        status_code = 200
    except Exception as error:
        message = f'error in on_jira_change: {error}'
        log_to_elk(message, data, index='elastic_logs', level='error')
        status_code = 200                                                   # don't return error 500 or Jira will keep sending it


    return {
                "isBase64Encoded": False      ,
                "statusCode"     : status_code,
                "headers"        : {}         ,
                "body"           : f'{message}'
           }