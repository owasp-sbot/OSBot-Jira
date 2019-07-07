from pbx_gs_python_utils.utils.Misc import Misc
from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment
from pbx_gs_python_utils.utils.slack.API_Slack_Dialog import API_Slack_Dialog

from osbot_jira.api.API_Issues import API_Issues

class Jira_View_Issue():
    def __init__(self, issue_id=None):
        self.issue_id    = issue_id
        self.api_issues  = API_Issues()
        self.issue       = None
        self.text        = None
        self.name        = "jira-view-issue"
        self.style       = 'primary'
        self.callback_id = 'jira-view-issue'
        self.slack_ui    = API_Slack_Attachment().set_callback_id(self.callback_id)

    # refactor this to base class
    def message_not_supported_action(self, action=''):
        return {"text": ':red_circle: Sorry, action not recognized : {0}'.format(action), "attachments": [], 'replace_original': False}

    def message_execution_error(self, error):
        return {"text": ':red_circle: Sorry, there was an error executing the requested action: {0}'.format(error), "attachments": [], 'replace_original': False}

    def handle_action(self,event):
        action       = Misc.array_pop(event.get('actions'), 0)
        action_value = Misc.get_value(action,'value')
        try:
            target = getattr(self,action_value)
        except:
            channel = event.get('channel').get('id')
            team_id = event.get('team').get('id')
            # temp code (refactor when adding full support for blocks)
            from osbot_jira.api.slack.API_Slack_Blocks import API_Slack_Blocks
            text = ':point_right: message not recognised: {0}'.format(action)
            API_Slack_Blocks().set_text(text).send_message(channel, team_id)

            return self.message_not_supported_action(action) # event.get('original_message'))

        try:
            return target(event)
        except Exception as error:
            return self.message_execution_error(error)

    def add_overflow(self, name, text, options):
        overflow = {  "name"    : name    ,
                      "text"    : text    ,
                      'state'   : 'an_state',
                      "action_id": 'an_action_id',
                      "block_id" : 'an_block_id',
                      "type"    : "select",
                      "options" : []      }
        for option in options:
            overflow['options'].append({ "text": option[0], "value": option[1]})
        self.slack_ui.actions.append(overflow)
        return self


    def add_button(self, text):
        button_id = text.lower().replace(' ','_')
        self.slack_ui.add_button(self.name, text,button_id, self.style)

    def create(self):
        self.issue = self.api_issues.issue(self.issue_id)
        if self.issue:
            key     = self.issue.get('Key')
            summary = self.issue.get('Summary')
            key_link = "{0}/browse/{1}".format(self.api_issues.server_url(), key)
            self.slack_ui.text = "<{0}|{1} - {2}>".format(key_link,key, summary)
            self.add_overflow('abc', 'chose one' ,[('aaaa','aaaa_1'),('bbbb','bbbb_2')])
            self.add_button('Edit Issue')
            self.add_button('An Replay')

        return self

    def render(self):


        return self.slack_ui.render()


    def get_actions_ui(self):
        self.create()
        if self.issue is None:
            return ':red_circle: Issue not found: `{0}`'.format(self.issue_id),[]
        #else:
            #text = ':point_right: Hello, here is the issue {0}  ... '.format(self.issue_id)
        return self.text, self.render()

    def an_replay(self, event):
        original_message = event.get('original_message')
        return {
            'text'            : "{0}".format(event), #original_message.get('text'),
            'attachments'     : original_message.get('attachments'),
            'replace_original': True
        }

    def edit_issue(self, event):
        return {
                    'text': 'in_edit_issue....: {0}'.format(event),
                    'replace_original': False
                }

