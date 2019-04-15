def run(event, context):
    from osbot_aws.apis.Lambda import load_dependency
    from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper import Slack_Commands_Helper


    data   = event.get('data')
    if data is not None:
        load_dependency('requests')
        channel = data.get('channel')
        team_id = data.get('team_id')
        params  = event.get('params')
        from pbx_gs_python_utils.gs_jira.GS_Bot_Jira_Commands import GS_Bot_Jira_Commands
        return Slack_Commands_Helper(GS_Bot_Jira_Commands).invoke(team_id, channel, params)