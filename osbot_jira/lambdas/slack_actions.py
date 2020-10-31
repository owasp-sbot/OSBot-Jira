from osbot_aws.Dependencies import load_dependencies

def run(event, context=None):
    load_dependencies('jira,elastic,slack,requests')
    from osbot_jira.api.slack.Slack_Actions import Slack_Actions
    #log_to_elk('in slack_actions:::::', f'{event}')

    return Slack_Actions().handle_request(event)

    #channel = event.get('channel').get('id')
    #team_id  = event.get('team').get('id')
    #return (team_id,channel)