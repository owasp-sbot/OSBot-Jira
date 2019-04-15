


def run(event, context):
    from osbot_aws.apis.Lambda                                  import load_dependency
    load_dependency('requests')

    from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper  import Slack_Commands_Helper
    from osbot_jira.api.GS_Bot_Jira_Commands                    import GS_Bot_Jira_Commands
    data   = event.get('data')
    if data is not None:

        channel = data.get('channel')
        team_id = data.get('team_id')
        params  = event.get('params')

        return Slack_Commands_Helper(GS_Bot_Jira_Commands).invoke(team_id, channel, params)