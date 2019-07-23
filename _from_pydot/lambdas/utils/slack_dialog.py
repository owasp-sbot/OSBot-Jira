from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack

def run(event, context):
    trigger_id = event['trigger_id']
    dialog     = event['dialog']
    return API_Slack().slack.api_call("dialog.open", trigger_id=trigger_id, dialog=dialog)
