from osbot_aws.apis.Lambda import load_dependency

def run(event, context):
    load_dependency('elastic-slack')
    load_dependency('requests')
    from osbot_jira.api.slack.Slack_Actions import Slack_Actions
    return Slack_Actions().handle_request(event)

    #channel = event.get('channel').get('id')
    #team_id  = event.get('team').get('id')
    #return (team_id,channel)