import json

from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc
from osbot_jira.api.API_Issues import API_Issues
from osbot_jira.api.jira_server.API_Jira import API_Jira
from osbot_jira.api.slack.blocks.API_Slack_Blocks import API_Slack_Blocks


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


    def create(self):
        self.issue = self.api_issues.issue(self.issue_id)
        if self.issue:
            key         = self.issue.get('Key')
            summary     = self.issue.get('Summary')
            latest_info = self.issue.get('Latest_Information')
            description = self.issue.get('Description')
            issue_type  = self.issue.get('Issue Type')
            key_link    = "{0}/browse/{1}".format(self.api_issues.server_url(), key)

            add_layout  = self.slack_blocks.add_layout_section

            text = "*{0}*: <{1}|{2} - {3}>".format(issue_type,key_link,key, summary)

            add_layout(self.issue_id).add_text(text).render()
            if latest_info:
                add_layout().add_text('*Latest Info:* \n{0}'.format(latest_info)).render()
            if description:
                add_layout().add_text('*Description:* \n{0}'.format(description)).render()

            actions_section = self.slack_blocks.add_layout_actions(self.action_id)
            footer_section  = self.slack_blocks.add_layout_context()

            self.add_select_with_issue_links()

            #actions_section.add_button('Edit Issue' , self.issue_id) \
            actions_section.add_button('Screenshot'   , self.issue_id) \
                           .add_button('Raw Data'     , self.issue_id) \
                           #.add_button('Change Status', self.issue_id)

            actions_section.render()


            #self.slack_blocks.blocks.append(self.block_select_with_issue_links(self.issue).blocks.pop())

            footer_items = [ 'Status: {0}'    .format(self.issue.get('Status')),
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
        else:
            self.slack_blocks.add_layout_section().add_text(':red_circle: Issue not found: `{0}`'.format(self.issue_id)).render()
        return self

    def send(self):
        return self.slack_blocks.send_message(self.channel, self.team_id)


    def create_and_send(self):
        self.send_message(':point_right: Loading data for issue: {0}'.format(self.issue_id))
        self.create()
        self.send()
        self.create_actions_with_transitions() # for now also add this?

    # def an_replay(self, event):
    #     original_message = event.get('original_message')
    #     return {
    #         'text'            : "{0}".format(event), #original_message.get('text'),
    #         'attachments'     : original_message.get('attachments'),
    #         'replace_original': True
    #     }

    def add_select_with_issue_links(self):
        issue_id = self.issue.get('Key')
        issue_links = self.issue.get('Issue Links')
        # view = API_Slack_Blocks()
        # view.add_text(':point_right: Here are the links for *{0}*: `{1}`'.format(issue_id, issue.get('Summary')))

        actions = self.slack_blocks.add_layout_actions(action_id='Jira_View_Issue')
        option_groups = []
        for issue_type, links in issue_links.items():
            options = []
            for link_issue_id in links:
                link_issue = self.api_issues.issue(link_issue_id)
                if link_issue:
                    link_summary = link_issue.get('Summary')
                    options.append((link_summary, link_issue_id))
            option_groups.append((issue_type, options))

        actions.add_select('Issue Links', option_groups=option_groups, action_id='view_issue')

        return actions.render()


    def create_actions_with_transitions(self):
        view = API_Slack_Blocks()

        transitions = self.api_jira.issue_next_transitions(self.issue_id)
        view.add_text(":arrow_right: `{0}` issue transitions available:".format(self.issue_id))
        actions = view.add_layout_actions(action_id='Jira_View_Issue')
        for key,value in transitions.items():
            action_id = "transition_to::{0}".format(value)
            value     = "{0}::{1}::{2}".format(self.issue_id,value,key)
            actions.add_button(key,action_id=action_id, value=value)
        actions.render()
        return view.send_message(self.channel, self.team_id)


    # callback methods

    def send_message(self,message):
        if self.channel:
            return slack_message(message, [], self.channel, self.team_id)
        else:
            return message

    def edit_issue(self,action):
        return self.send_message(':point_right: In edit issue:{0}'.format(action))

    def issue_links(self, action):
        issue_id = action.get('value')
        issue = self.api_issues.issue(issue_id)
        if issue:
            view = self.block_select_with_issue_links(issue)
            return view.send_message(self.channel,self.team_id)

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
            self.create_actions_with_transitions()
        except Exception as error:
            self.send_message(':red_circle: Error in change_status: {0}'.format(error))

    def transition_to(self,action):
        value_split     = action.get('value').split('::')
        issue_id        = Misc.array_pop(value_split,0)
        transition_to   = Misc.array_pop(value_split,0)
        transition_name = Misc.array_pop(value_split, 0)
        #self.send_message('Changing status of `{0}` to `{1}`'.format(issue_id, transition_name))
        try:
            self.api_jira.issue_transition_to_id(issue_id, transition_to)
            self.send_message(':white_check_mark: Changed `{0}` status to: {1}'.format(issue_id, transition_name))
            self.issue_id = issue_id
            self.create_actions_with_transitions()
        except Exception as error:
            self.send_message(':red_circle: Error in transition_to: {0}'.format(error))



