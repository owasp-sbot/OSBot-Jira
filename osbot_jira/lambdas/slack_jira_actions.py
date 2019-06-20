from osbot_aws.apis.Lambda import load_dependency

def run(event, context):
    load_dependency('jira')
    data    = event.get('data')
    channel = event.get('channel')
    team_id = event.get('team_id')
    from osbot_jira.api.slack.Slack_Dialog_Submissions import Slack_Dialog_Submissions
    return Slack_Dialog_Submissions(data, channel,team_id).handle()