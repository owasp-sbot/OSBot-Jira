from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
from pbx_gs_python_utils.utils.slack.API_Slack_Dialog import API_Slack_Dialog

from osbot_jira.api.slack.dialogs.Jira_Create_Issue import Jira_Create_Issue


class Slack_Actions:

    def callback_button_dialog_test(self, data):
        trigger_id = data.get('trigger_id')
        #slack_dialog = API_Slack_Dialog().test_render()
        slack_dialog = Jira_Create_Issue().setup().render()
        API_Slack().slack.api_call("dialog.open", trigger_id=trigger_id, dialog=slack_dialog)


        return {"text": "Opening test dialog ...", "attachments": [], 'replace_original': False}


    def process_action(self, data):
        callback_id = data['callback_id']
        #if callback_id == 'view-jira-issue'     : return self.callback_view_jira_issue    (data)
        #if callback_id == 'change-issue-status' : return self.callback_change_issue_status(data)
        #if callback_id == 'jira-dialog-action'  : return self.callback_jira_dialog_action (data)
        if callback_id == 'button-dialog-test'  : return self.callback_button_dialog_test (data)
        #if callback_id == 'issue-suggestion'    : return self.process_dialog_suggestion   (data, "text")

        text             = ':red_circle: requested action currently not supported: `{0}`'.format(callback_id)
        replace_original = False
        return { 'text': text, 'attachments':[] , 'replace_original': replace_original }

    def handle_dialog_submission(self, data):
        callback_id = data['callback_id']
        channel     = data['channel']['id']
        team_id     = data['team']['id']
        user_id     = data['user']['id']

        # if callback_id =='jira-graph-chooser':
        #     graph_name = data['submission'].get('graph_name')
        #     Lambdas('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke_async({"params": ["graph", graph_name], "user": user_id, "channel": channel})
        #
        # elif callback_id == 'jira-view-issue-links':
        #     self.handle_callback_jira_view_issue_links(data)
        #
        # elif callback_id == 'jira-view-issue-dialogue':
        #     slack_message('jira-view-issue-dialogue: {0}'.format(data),[], channel)
        #     key     = data.get('submission').get('key')
        #     result  = Lambdas('pbx_gs_python_utils.lambdas.gs.elastic_jira').invoke({"params": ["issue", key], "user": user_id, "channel": channel})
        #     slack_message(result.get('text'), result.get('attachments'), channel)
        #
        # elif callback_id == 'issue-search-dialog':
        #     self.handle_callback_issue_search_dialog(data)
        #
        # else:
        error_message = ":red_circle: Dialog callback_id not supported: {0}".format(callback_id)
        slack_message(error_message, [], channel,team_id)
            #self.api_slack.send_message(error_message, channel=channel)
        return {}
        
        return {
                  "errors": [
                    {
                      "name": "name_1",
                      "error": "this is working 123 abc"
                    },
                    {
                      "name": "username",
                      "error": "Uh-oh. This username has been taken!"
                    }
                  ]
                }

    def handle_request(self, event):
        channel = event['channel']['id']
        team_id = event['team']['id']

        event_type = event.get('type')

        slack_message(event_type,[], channel, team_id)

        if   event_type == 'interactive_message' : return self.process_action (event)
        elif event_type == 'dialog_submission'   : return self.handle_dialog_submission (event)

        #elif 'type%22%3A%22dialog_submission'   in body: return self.process_dialog_submission (self.decode_body_with_payload(body))
        #elif 'type%22%3A%22message_action'      in body: return self.process_interactive_action(self.decode_body_with_payload(body))
        #elif 'type%22%3A%22dialog_suggestion'   in body: return self.process_dialog_suggestion (self.decode_body_with_payload(body), "label")
        else:
            return ":red_circle: Unsupported slack action type: {0}".format(event_type)