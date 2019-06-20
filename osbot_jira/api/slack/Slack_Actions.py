from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message, log_to_elk
from pbx_gs_python_utils.utils.Misc import Misc
from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
from pbx_gs_python_utils.utils.slack.API_Slack_Dialog import API_Slack_Dialog

from osbot_jira.api.slack.Jira_Slack_Actions import Jira_Slack_Actions
from osbot_jira.api.slack.Slack_Dialog_Submissions import Slack_Dialog_Submissions
from osbot_jira.api.slack.dialogs.Jira_Create_Issue import Jira_Create_Issue


class Slack_Actions:

    def callback_button_dialog_test(self, data):
        trigger_id = data.get('trigger_id')
        #slack_dialog = API_Slack_Dialog().test_render()
        slack_dialog = Jira_Create_Issue().setup().render()
        API_Slack().slack.api_call("dialog.open", trigger_id=trigger_id, dialog=slack_dialog)


        return {"text": "Opening test dialog ...", "attachments": [], 'replace_original': False}


    def handle_interactive_message(self, data):
        callback_id = data['callback_id']
        #if callback_id == 'view-jira-issue'     : return self.callback_view_jira_issue    (data)
        #if callback_id == 'change-issue-status' : return self.callback_change_issue_status(data)
        #if callback_id == 'jira-dialog-action'  : return self.callback_jira_dialog_action (data)
        if callback_id == 'button-dialog-test'  : return self.callback_button_dialog_test (data)
        #if callback_id == 'issue-suggestion'    : return self.process_dialog_suggestion   (data, "text")
        if callback_id == 'select_remote_1234'  : return self.handle_dialog_suggestion (data)


        actions = {'jira-slack-actions' : Jira_Slack_Actions}

        if actions.get(callback_id):
            handler = actions.get(callback_id)
            return handler().handle_action(data)

        replace_original = False

        if callback_id == 'gs_detect_slack':
            #return {'text': 'here: {0}'.format(data), 'attachments': [], 'replace_original': replace_original}
            try:
                #channel = data['channel']['id']
                #team_id = data['team']['id']
                #slack_message('in gs_detect_slack handled: {0}'.format(data), [], channel, team_id)
                text = Lambda('gs_detect.lambdas.alerting_slack_callbacks').invoke(data)
                return {'text': text,  'attachments': [], 'replace_original': replace_original}
            except Exception as error:
                return {'text': "Execution error: {0}".format(error), 'attachments': [], 'replace_original': replace_original}

        text             = ':red_circle: requested action currently not supported: `{0}`'.format(callback_id)
        return { 'text': text, 'attachments':[] , 'replace_original': replace_original }

    def handle_dialog_submission(self, event):

        channel = event['channel']['id']
        team_id = event['team']['id']
        #user         = "{0} - {1}".format(data['user']['name'],data['user']['id'])
        data    = {
                      'channel'      : event.get('channel'     ),
                      'team_id'      : event.get('team'        ),
                      'user'         : event.get('user'        ),
                      'callback_id'  : event.get('callback_id' ),
                      'submission'   : event.get('submission'  ),
                      'action_ts'    : event.get('action_ts'   ),
                      'response_url' : event.get('response_url'),

                   }

        log_to_elk('Slack_Actions.handle_dialog_submission', data=data, index='slack_interaction', category='OSBot-jira')

        Slack_Dialog_Submissions(data,channel, team_id).handle()
        # log_to_elk(submission,index='slack_interaction')
        #
        # payload = {
        #     "index": 'slack_interaction',
        #     "level": 'info',
        #     "message": 'Slack_Actions.handle_dialog_submission',
        #     "category": 'bc',
        #     "data": submission
        # }
        #
        # from osbot_aws.apis.Lambda import Lambda
        # return Lambda('pbx_gs_python_utils.lambdas.utils.log_to_elk').invoke(payload)
        # slack_message("{0}".format(submission), [], channel, team_id)

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
        #message = ':point_right: message received: {0}'.format(data)

        #error_message = ":red_circle: Dialog callback_id not supported: {0}".format(callback_id)
        #slack_message(error_message, [], channel,team_id)
            #self.api_slack.send_message(error_message, channel=channel)
        return {}

        # return {
        #           "errors": [
        #             {
        #               "name": "name_1",
        #               "error": "this is working 123 abc"
        #             },
        #             {
        #               "name": "username",
        #               "error": "Uh-oh. This username has been taken!"
        #             }
        #           ]
        #         }

    def handle_dialog_suggestion(self, data):
        tmp = Misc.random_string_and_numbers()
        return {
                    "options": [
                        {
                            "text": "Unexpected sentience: {0}".format(tmp),
                            "value": "AI-2323"
                        },
                        {
                            "text": "Bot biased toward other bots: {0}".format(data.get('value')),
                            "value": "SUPPORT-42"
                        },
                        {
                            "text": "Bot broke my toaster",
                            "value": "IOT-75"
                        }
                    ]
                }

    def handle_request(self, event):
        channel = event['channel']['id']
        team_id = event['team']['id']

        event_type = event.get('type')



        if   event_type == 'interactive_message' : return self.handle_interactive_message (event)
        elif event_type == 'dialog_submission'   : return self.handle_dialog_submission (event)
        #elif event_type == 'dialog_suggestion'   : return self.handle_dialog_suggestion(event)

        elif event_type == 'dialog_cancellation': return {}

        #elif 'type%22%3A%22dialog_submission'   in body: return self.process_dialog_submission (self.decode_body_with_payload(body))
        #elif 'type%22%3A%22message_action'      in body: return self.process_interactive_action(self.decode_body_with_payload(body))
        #elif 'type%22%3A%22dialog_suggestion'   in body: return self.process_dialog_suggestion (self.decode_body_with_payload(body), "label")
        else:
            #slack_message("Event_Type: {0} ```{1}```".format(event_type, event), [], channel, team_id)
            slack_message(":red_circle: Unsupported slack action type: {0}".format(event_type), [], 'DDKUZTK6X')
            return ":red_circle: Unsupported slack action type: {0}".format(event_type)