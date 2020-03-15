from gw_bot.api.API_Slack import API_Slack
from gw_bot.api.slack.API_Slack_Attachment import API_Slack_Attachment
from osbot_jira.api.slack.Slack_Jira_Search import Slack_Jira_Search
from osbot_jira.api.slack.dialogs.Jira_Create_Issue import Jira_Create_Issue
from osbot_utils.utils import Misc


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

    def create(self):                                           # this is where the current buttons exist
        self.buttons_ui.set_callback_id(self.callback_id)
        self.add_button('Create Issue')
        #self.add_button('Search')
        #self.add_button('Search')

        return self

    def message_not_supported_action(self, action=''):
        return {"text": ':red_circle: Sorry, action not recognized (in Jira_Slack_Actions) : {0}'.format(action), "attachments": [], 'replace_original': False}

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
        API_Slack(channel,team).slack.dialog_open(trigger_id=trigger_id, dialog=slack_dialog)

        return {"text": ":point_right: Opening `Create Issue` dialog".format(channel, team), "attachments": [], 'replace_original': False}



    def search(self, event):
        #channel    = event.get('channel').get('id')
        #team       = event.get('team').get('id')
        (text, attachments) = Slack_Jira_Search().get_drop_box_ui()
        return {"text": text, "attachments": attachments,'replace_original': False}

        #slack_message(text, attachments, channel)
        # trigger_id = event.get('trigger_id')

        #
        # from pbx_gs_python_utils.utils.slack.API_Slack_Dialog import API_Slack_Dialog
        # dialog = API_Slack_Dialog()
        # dialog.callback_id = 'issue-search-dialog'
        # dialog.title       = 'Search for Issue'
        # dialog.add_element_select_external("Find issue", "key", "Search ELK for issue in indexes: jira and it_assets")
        # dialog.add_element_select         ("View Type"       , "view-type", [
        #                                                                         ("Table"                         , "table"                       ),
        #                                                                         #("Issue Links all (depth 1)"     , "issue-links-all-depth-1"     ),
        #                                                                         ("Issue Links (vuln path)"       , "issue-links-vuln-path"       ),
        #                                                                         ("Issue Links (stakeholder path)", "issue-links-stakeholder-path")]
        #                                                                         #('Issue Links (view all)'        , 'issue-links-view-all'        )]
        #                                                      , "table")
        # dialog.add_element_select         ("View engine"     , "view-engine", [("Normal", "normal"),("With all links","with-all-links")], "normal")
        #
        # slack_dialog = dialog.render()
        # API_Slack(channel, team).slack.api_call("dialog.open", trigger_id=trigger_id, dialog=slack_dialog)
        # return {"text": "Opening Search dialog", "attachments": [], 'replace_original': False}
