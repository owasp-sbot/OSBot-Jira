from pbx_gs_python_utils.utils.Misc import Misc
from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment

from osbot_jira.api.slack.dialogs.Jira_Create_Issue import Jira_Create_Issue


class Jira_Slack_Actions:

    def __init__(self):
        self.name        = "jira-actions"
        self.style       = 'primary'
        self.callback_id = 'jira-slack-actions'
        self.buttons_ui  = API_Slack_Attachment()

    def get_actions_ui(self):
        self.create()
        text        = ':point_right: Hello, here are the currently supported Jira Actions'
        return text, self.buttons_ui.render()

    def add_button(self, text):
        #"jira-actions", "Create Issue", "create-issue", ""
        button_id = text.lower().replace(' ','_')
        self.buttons_ui.add_button(self.name, text,button_id, self.style)

    def create(self):
        self.buttons_ui.set_callback_id(self.callback_id)
        self.add_button('Create Issue')
        return self

    def message_not_supported_action(self, action=''):
        return {"text": ':red_circle: Sorry, action not recognized : {0}'.format(action), "attachments": [], 'replace_original': False}

    def message_execution_error(self, error):
        return {"text": ':red_circle: Sorry, there was an error executing the requested action: {0}'.format(error), "attachments": [], 'replace_original': False}

    def handle_action(self,event):
        action = Misc.get_value(Misc.array_pop(event.get('actions'),0), 'value')
        try:
            target = getattr(self,action)
        except:
            return self.message_not_supported_action(action)

        try:
            return target(event)
        except Exception as error:
            return self.message_execution_error(error)


    def create_issue(self, event):
        trigger_id = event.get('trigger_id')
        channel    = event.get('channel').get('id')
        team       = event.get('team'   ).get('id')
        slack_dialog = Jira_Create_Issue().setup().render()
        API_Slack(channel,team).slack.api_call("dialog.open", trigger_id=trigger_id, dialog=slack_dialog)
        return {"text": "Opening Create issue pop up dialog in {0} and {1}".format(channel, team), "attachments": [], 'replace_original': False}

