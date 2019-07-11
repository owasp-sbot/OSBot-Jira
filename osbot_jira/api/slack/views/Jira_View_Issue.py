import json

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc
from osbot_jira.api.API_Issues import API_Issues
from osbot_jira.api.jira_server.API_Jira import API_Jira
from osbot_jira.api.slack.blocks.API_Slack_Blocks import API_Slack_Blocks
from osbot_jira.api.slack.dialogs.Jira_Edit_Issue import Jira_Edit_Issue


class Jira_View_Issue():
    def __init__(self, issue_id=None, channel=None,team_id=None, event=None):
        self.issue_id    = issue_id
        self.channel     = channel
        self.team_id     = team_id
        self.event       = event
        self.api_issues  = API_Issues()
        self.api_jira    = API_Jira()
        self.issue       = None
        self.action_id   = 'Jira_View_Issue'
        self.slack_blocks = API_Slack_Blocks()

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
            from osbot_jira.api.slack.blocks.API_Slack_Blocks import API_Slack_Blocks
            text = ':point_right: message not recognised: {0}'.format(action)
            API_Slack_Blocks().set_text(text).send_message(channel, team_id)

            return self.message_not_supported_action(action) # event.get('original_message'))

        try:
            return target(event)
        except Exception as error:
            return self.message_execution_error(error)

    def load_issue(self, issue_id=None):
        if issue_id:
            self.issue_id = issue_id
        self.issue = self.api_issues.issue(self.issue_id)
        return self

    def create(self):
        self.load_issue()
        if self.issue:
            key         = self.issue.get('Key')
            summary     = self.issue.get('Summary')
            latest_info = self.issue.get('Latest_Information')
            description = self.issue.get('Description')
            issue_type  = self.issue.get('Issue Type')
            key_link    = "{0}/browse/{1}".format(self.api_issues.server_url(), key)

            add_layout  = self.slack_blocks.add_layout_section

            text = "*{0}*:\n<{1}|{2} - {3}>".format(issue_type,key_link,key, summary)

            add_layout(self.issue_id).add_text(text).render()
            if latest_info:
                add_layout().add_text('*Latest Info:* \n{0}'.format(latest_info)).render()
            if description:
                add_layout().add_text('*Description:* \n{0}'.format(description)).render()

            actions_section = self.slack_blocks.add_layout_actions(self.action_id)
            footer_section  = self.slack_blocks.add_layout_context()

            actions_section.add_button('Edit Issue' , self.issue_id) \
                           .add_button('Screenshot', self.issue_id) \
                           .add_button('Raw Data', self.issue_id) \
                        # .add_button('Change Status', self.issue_id)

            actions_section.render()


            self.add_block_actions_with_transitions(self.slack_blocks)

            self.add_select_with_issue_links()

            self.slack_blocks.add_divider()
            footer_items = [ #'Status: {0}'    .format(self.issue.get('Status')),
                             'Rating: {0}'    .format(self.issue.get('Rating')),
                             'Priority: {0}'  .format(self.issue.get('Priority')),
                             'Issue Type: {0}'.format(self.issue.get('Issue Type')),
                             'Assignee: {0}'.format(self.issue.get('Assignee')),
                             'Labels: {0}'.format(self.issue.get('Labels')),
                             'Creator: {0}'.format(self.issue.get('Creator')),
                             'Created: {0}'.format(self.issue.get('Created').split('T').pop(0)),
                             'Updated: {0}'.format(self.issue.get('Updated').split('T').pop(0))
                            ]
            footer_section.add_texts(footer_items).render()




            #issue_data = "```{0}```".format(json.dumps(self.issue,indent=4))
            #self.slack_blocks.add_layout_section().add_text(issue_data).render()

            #self.slack_ui.text = "<{0}|{1} - {2}>".format(key_link,key, summary)
            #self.add_overflow('abc', 'chose one' ,[('aaaa','aaaa_1'),('bbbb','bbbb_2')])
            #self.add_button('Edit Issue')
            #self.add_button('An Replay')

            self.slack_blocks.add_attachment({'text':'Issue *{0}* Status: `{1}`'.format(self.issue_id, self.issue.get('Status')),'color':'good'})
        else:
            self.slack_blocks.add_layout_section().add_text(':red_circle: Issue not found: `{0}`'.format(self.issue_id)).render()
        return self

    def send(self):
        result = self.slack_blocks.send_message(self.channel, self.team_id)
        if type(result) == dict and result.get('ok') is False:
            error_messages = result.get('response_metadata').get('messages')
            self.send_message(':red_circle: Error in `Jira_View_Issue.send`; ```{0}```'.format(error_messages))
        return result


    def create_and_send(self):
        self.send_message(':point_right: *Loading data for issue: `{0}`* :point_left:'.format(self.issue_id))
        self.create()
        return self.send()

    # def an_replay(self, event):
    #     original_message = event.get('original_message')
    #     return {
    #         'text'            : "{0}".format(event), #original_message.get('text'),
    #         'attachments'     : original_message.get('attachments'),
    #         'replace_original': True
    #     }

    def add_select_with_issue_links(self):
        issue_links = self.issue.get('Issue Links')
        if issue_links:
            self.slack_blocks.add_text(':link: View Linked issue')
            actions = self.slack_blocks.add_layout_actions(action_id='Jira_View_Issue')
            option_groups = []
            for issue_type, links in issue_links.items():
                options = []
                for link_issue_id in links:
                    link_issue = self.api_issues.issue(link_issue_id)
                    if link_issue:
                        link_summary    = link_issue.get('Summary')
                        link_issue_type = link_issue.get('Issue Type')
                        text            = "{0} - {1}".format(link_issue_type, link_summary)[0:75]

                        options.append((text , link_issue_id))
                options = []
                print(options)
                option_groups.append((issue_type, options))

            actions.add_select('Issue Links', option_groups=option_groups)#, action_id='view_issue')

            return actions.render()

    def create_ui_actions_with_transitions(self ,issue_id=None,current_status=None):
        if issue_id:
            self.issue_id = issue_id
        view = API_Slack_Blocks()
        self.add_block_actions_with_transitions(view, current_status)
        return view.send_message(self.channel, self.team_id)

    def add_block_actions_with_transitions(self,view,current_status=None):
        if self.issue is None:
            self.issue = self.api_issues.issue(self.issue_id)
        if current_status is None:                                              # this helps with the situation when the issue has just been updated but the data has not reached out to ELK
            current_status = self.issue.get('Status')
        transitions = self.api_jira.issue_next_transitions(self.issue_id)
        view.add_text(":arrow_right: Change issue status to:")
        actions = view.add_layout_actions(action_id='Jira_View_Issue')
        for key, value in transitions.items():
            if key != current_status:
                action_id = "transition_to::{0}".format(value)
                value = "{0}::{1}::{2}".format(self.issue_id, value, key)
                actions.add_button(key, value=value, action_id=action_id)
        return actions.render()



    def create_ui_edit_issue_field(self):
        view = API_Slack_Blocks()
        self.add_block_edit_issue_field(view)
        return view.send_message(self.channel, self.team_id)

    def add_block_edit_issue_field(self,view):
        view.add_text(":arrow_right: which field to edit from {0}`".format(self.issue_id))
        self.issue = self.api_issues.issue(self.issue_id)
        if self.issue:
            fields = set(self.issue)
            action_id = 'Jira_View_Issue::edit_field::{0}'.format(self.issue_id)
            view.add_select(action_id, 'Field to edit', fields)

    # callback methods

    def send_message(self,message):
        if self.channel:
            return slack_message(message, [], self.channel, self.team_id)
        else:
            return message

    def edit_field(self,action):

        selected_option = action.get('selected_option')
        field           = selected_option.get('text').get('text')
        issue_id        = action.get('action_id').split('::').pop(3)
        trigger_id      = self.event.get('trigger_id')


        from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack

        slack_dialog = Jira_Edit_Issue(issue_id, field).setup().render()
        API_Slack().slack.api_call("dialog.open", trigger_id=trigger_id, dialog=slack_dialog)
        #return self.send_message(':point_right: result {0}'.format(result))
        #result
        #return self.send_message(':point_right: ...In edit field: {0} : :{1}  {2}'.format(issue_id,field,trigger_id))

    def issue_links(self,action):
        self.view_issue(action)

    def screenshot(self, action):
        issue_id = action.get('value')
        payload = {'params': [issue_id], 'channel': self.channel, 'team_id': self.team_id}
        Lambda('osbot_jira.lambdas.elastic_jira').invoke_async(payload)

    def raw_data(self, action):
        issue_id = action.get('value')
        issue = API_Issues().issue(issue_id)
        if issue:
            issue_data = "```{0}```".format(json.dumps(issue, indent=4))
            return self.send_message(issue_data)

    def view_issue(self,action):
        issue_id = action.get('value')
        if issue_id is None:
            selected_option = action.get('selected_option')
            if selected_option:
                issue_id = selected_option.get('value')
        if issue_id:
            payload = {'params': ['issue_new', issue_id], 'channel': self.channel, 'team_id': self.team_id}
            Lambda('osbot_jira.lambdas.elastic_jira').invoke_async(payload)
        else:
            self.send_message(':red_circle: Error in View Issue, no issue id found in action :{0}'.format(action))

    def change_status(self, action):
        try:
            self.issue_id = action.get('value')
            self.create_ui_actions_with_transitions()
        except Exception as error:
            self.send_message(':red_circle: Error in change_status: {0}'.format(error))

    def edit_issue(self,action):
        try:
            self.issue_id = action.get('value')
            self.create_ui_edit_issue_field()
        except Exception as error:
            self.send_message(':red_circle: Error in change_status: {0}'.format(error))

    def transition_to(self,action):
        value_split     = action.get('value').split('::')
        issue_id        = Misc.array_pop(value_split,0)
        transition_to   = Misc.array_pop(value_split,0)
        transition_name = Misc.array_pop(value_split, 0)
        try:
            self.api_jira.issue_transition_to_id(issue_id, transition_to)
            self.send_message(':white_check_mark: Changed `{0}` status to: *{1}*. Here are the new transitions available '.format(issue_id, transition_name))
            self.create_ui_actions_with_transitions(issue_id, transition_name)
        except Exception as error:
            self.send_message(':red_circle: Error in transition_to: {0}'.format(error))



