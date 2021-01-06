import json

from gw_bot.api.API_Slack import API_Slack
from osbot_aws.apis.Lambda                          import Lambda
from osbot_aws.helpers.Lambda_Helpers import slack_message, log_to_elk
from osbot_utils.utils import Misc

from osbot_jira.api.slack.views.Jira_Slack_Actions  import Jira_Slack_Actions
from osbot_jira.api.slack.Slack_Jira_Search         import Slack_Jira_Search
from osbot_jira.api.slack.Slack_Message_Action      import Slack_Message_Action
from osbot_jira.api.slack.dialogs.Jira_Create_Issue import Jira_Create_Issue
from osbot_jira.api.slack.views.Jira_View_Issue import Jira_View_Issue


class Slack_Actions:

    def callback_button_dialog_test(self, data):
        trigger_id = data.get('trigger_id')
        #slack_dialog = API_Slack_Dialog().test_render()
        slack_dialog = Jira_Create_Issue().setup().render()
        API_Slack().slack.dialog_open(trigger_id=trigger_id, dialog=slack_dialog)

        return {"text": "Opening test dialog ...", "attachments": [], 'replace_original': False}


    def handle_interactive_message(self, data):
        callback_id = data['callback_id']
        #if callback_id == 'view-jira-issue'     : return self.callback_view_jira_issue    (data)
        #if callback_id == 'change-issue-status' : return self.callback_change_issue_status(data)
        #if callback_id == 'jira-dialog-action'  : return self.callback_jira_dialog_action (data)
        if callback_id == 'button-dialog-test'  : return self.callback_button_dialog_test (data)
        #if callback_id == 'issue-suggestion'    : return self.process_dialog_suggestion   (data, "text")
        if callback_id == 'select_remote_1234'  : return self.handle_dialog_suggestion (data)


        actions = {
                    'jira-slack-actions' : Jira_Slack_Actions,
                    'jira-view-issue'    : Jira_View_Issue
                   }
        if actions.get(callback_id):
            handler = actions.get(callback_id)
            return handler().handle_action(data)


        replace_original = False
        # todo: refactor to handler method
        if callback_id == 'gs_detect_slack':
            try:
                #text = Lambda('gs_detect.lambdas.alerting_slack_callbacks').invoke(data)
                #return {'text': text,  'attachments': [], 'replace_original': replace_original}
                Lambda('gs_detect.lambdas.alerting_slack_callbacks').invoke_async(data)
                return {}
            except Exception as error:
                return {'text': "Execution error: {0}".format(error), 'attachments': [], 'replace_original': replace_original}

        if callback_id == 'jira_search_select_box':
            return Slack_Jira_Search().from_select_box(data)
            #return {'text': text, 'attachments': [], 'replace_original': replace_original}

        text  = ':red_circle: Requested action currently not supported: `{0}`'.format(callback_id)

        #channel = data['channel']['id']
        #team_id = data['team']['id']
        #slack_message(text, [], channel, team_id)

        return { 'text': text, 'attachments': [] , 'replace_original': replace_original }

    def handle_block_action(self,event):        # todo: refactor in to separate method handler (specially when adding the lambda capability)
        channel  = Misc.get_value(Misc.get_value(event,'channel'),'id')
        team_id  = Misc.get_value(Misc.get_value(event,'team'),'id')
        actions  = event.get('actions')
        handlers = { 'Jira_View_Issue': Jira_View_Issue}
        def send_message(message):
            if channel:
                slack_message(message,[], channel, team_id)
            else:
                return message
        try:
            for action in actions:
                split_action  = action.get('action_id').split('::')
                action_type   = Misc.array_get(split_action, 0)
                action_class  = Misc.array_get(split_action, 1)
                action_method = Misc.array_get(split_action, 2)
                if action_type == 'class_method':
                    if action_class and action_method:
                        target = handlers.get(action_class)
                        if target:
                            try:
                                method = getattr(target, action_method)
                                #slack_message(':point_right: Invoking method `{0}.{1}`'.format(action_class,action_method), [], channel, team_id)
                                try:
                                    target_obj = target(channel=channel,team_id=team_id, event=event)
                                    return method(target_obj, action)
                                except Exception as error:
                                    return send_message(':red_circle: Error in `handle_block_action` invocation of method `{0}.{1}`: `{2}`'.format(action_class,action_method, error))
                            except:
                                return send_message(':red_circle: Error in `handle_block_action` could not resolve method: `{0}.{1}`'.format(action_class,action_method))
                        else:
                            return send_message(':red_circle: Error in `handle_block_action` could not resolve class action: `{0}`'.format(action_class))
                    else:
                        return send_message(':red_circle: Error in `handle_block_action` could not resolve action: `{0}`'.format(action))
                #elif action_type == 'lambda':
                else:
                    return send_message(':red_circle: Error in `handle_block_action` un-supported action type: `{0}`'.format(split_action))
            return None
        except Exception as error:
            return send_message(":red_circle: error in handle_block_action: `{0}` . Actions value was `{1}`".format(error,actions))
        #text = 'here'
        #return {'text': text, 'attachments': [], 'replace_original': replace_original}

    def handle_message_action(self, event):
        channel     = event['channel']['id']
        team_id     = event['team']['id']
        callback_id = event.get('callback_id')
        message     = event.get('message')
        trigger_id  =  event.get('trigger_id'),
        #text       = message.get('text')
        #slack_message('in handle_message_action: `{0}` with message `{1}`'.format(callback_id,message), [], channel, team_id)
        # payload = { "channel"    : channel     ,
        #             "team_id"    : team_id     ,
        #             'callback_id': callback_id ,
        #             "data"       : message     }

        if callback_id == 'jira-create-issue-from-slack-message':
            Slack_Message_Action(message, trigger_id, channel, team_id).jira_create_issue_from_slack_message()


        #result = Lambda('osbot_jira.lambdas.slack_jira_actions').invoke(payload)  # calling lambda that handles submissions
        #slack_message("result {0}".format(result), [], channel,team_id)

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



        payload =  { "channel": channel,
                     "team_id": team_id,
                     "data"   : data  }
        Lambda('osbot_jira.lambdas.slack_jira_actions').invoke_async(payload) # calling lambda that handles submissions

        return {}

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

    # todo: see if there is a better way to do this
    def fix_slack_encoding(self, event):
        try:
            event_str   = json.dumps(event)
            event_fixed = event_str   .replace('+', ' ')                    # fix the issue that slack replaces spaces with +
            event_fixed = event_fixed.replace('“', '"').replace('”','"')    # fix " (double quote)
            event_fixed = event_fixed.replace('‘', "'").replace('’', "'")   # fix " (single quote)
            return json.loads(event_fixed)
        except:
            return event

    def handle_request(self, event):

        event = self.fix_slack_encoding(event)
        channel = event.get('channel', {}).get('id')
        team_id = event.get('team'   , {}).get('id')

        #slack_message('in handle request',[] , channel, team_id)

        event_type = event.get('type')

        if   event_type == 'interactive_message' : return self.handle_interactive_message (event)
        elif event_type == 'dialog_submission'   : return self.handle_dialog_submission (event)
        elif event_type == 'message_action'      : return self.handle_message_action(event)
        elif event_type == 'block_actions'       : return self.handle_block_action(event)
        elif event_type == 'dialog_cancellation' : return {}
        #elif event_type == 'dialog_suggestion'   : return self.handle_dialog_suggestion(event)
        #elif 'type%22%3A%22dialog_submission'   in body: return self.process_dialog_submission (self.decode_body_with_payload(body))
        #elif 'type%22%3A%22message_action'      in body: return self.process_interactive_action(self.decode_body_with_payload(body))
        #elif 'type%22%3A%22dialog_suggestion'   in body: return self.process_dialog_suggestion (self.decode_body_with_payload(body), "label")
        else:
            #slack_message("Event_Type: {0} ```{1}```".format(event_type, event), [], channel, team_id)
            slack_message(":red_circle: Unsupported slack action type: {0}".format(event_type), [], channel, team_id)
            return ":red_circle: Unsupported slack action type: {0}".format(event_type)