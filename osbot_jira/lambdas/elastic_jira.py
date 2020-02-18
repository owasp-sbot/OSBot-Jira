from gw_bot.helpers.Lambda_Helpers import log_to_elk, slack_message
from osbot_aws.Dependencies import load_dependencies


def run(event, context):
    load_dependencies('elastic,slack,requests,jira')
    try:
        from osbot_jira.api.GS_Bot_Jira import GS_Bot_Jira
        result = GS_Bot_Jira().handle_request(event)                         # invoke lambda main handler method

        log_to_elk("[elastic jira][result]: {0}".format(result))
        channel = event.get('channel')
        team_id = event.get('team_id')

        if (result is not None) and (channel is not None):
            slack_message(result.get('text'), result.get('attachments'), channel=channel, team_id=team_id)
        else:
            return result
    except Exception as error:
        log_to_elk("[elastic jira][Error]: {0}".format(error) , level='error')