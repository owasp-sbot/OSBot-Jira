from gs_elk.API_Jira_Dialog import API_Jira_Dialog
from utils.Lambdas_Helpers import slack_message, log_to_elk


def run(event, context):
    try:
        data    = event.get('data')
        type    = event.get('type')
        if type == 'jira_slash_command': return API_Jira_Dialog().handle_jira_slash_command (data)
        if type == 'dialog_submission' : return API_Jira_Dialog().handle_dialog_submission  (data)
        if type == 'jira_dialog_action': return API_Jira_Dialog().handle_jira_dialog_action (data)
        if type == 'button_dialog_test': return API_Jira_Dialog().handle_button_dialog_test (data)
        return { "text": 'Unrecognised command: {0}'.format(type), "attachments": [], 'replace_original': False }
    except Exception as error:
        error_message = 'Error in jira_dialog Lambda: {0}'.format(error)
        log_to_elk(error_message, level='error')
        return {"text": error_message, "attachments": []}
