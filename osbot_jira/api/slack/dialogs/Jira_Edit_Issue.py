from pbx_gs_python_utils.utils.slack.API_Slack_Dialog import API_Slack_Dialog

from osbot_jira.api.API_Issues import API_Issues


class Jira_Edit_Issue(API_Slack_Dialog):

    def __init__(self, issue_id, field):
        super().__init__()
        self.issue_id     = issue_id
        self.field        = field
        self.issue        = None
        self.api_issues   = API_Issues()
        self.submit_label = 'Save'

    def setup(self):
        self.callback_id = 'jira_edit_issue'
        self.title       = 'Edit {0}'.format(self.issue_id)
        self.issue       = self.api_issues.issue(self.issue_id)
        if not self.issue:
            self.add_element_text('ERROR - Issue not found: {0}'.format(self.issue_id))
        else:
            key   = "{0}::{1}".format(self.issue_id, self.field)
            value =self.issue.get(self.field)
            #todo: add different type of edit fields based on field name
            self.add_element_textarea(self.field, key, value)


        return self

    def render(self):
        return {
                    "callback_id"      : self.callback_id     ,
                    "title"            : self.title           ,
                    "submit_label"     : self.submit_label    ,
                    "notify_on_cancel" : self.notify_on_cancel,
                    "elements"         : self.elements        }