from pbx_gs_python_utils.utils.slack.API_Slack_Dialog import API_Slack_Dialog


class Jira_Create_Issue(API_Slack_Dialog):

    def __init__(self):
        super().__init__()

    def setup(self):
        self.callback_id    = 'issue-suggestion'
        self.title          = 'This is a test'
        self.add_element_text("label 1", "name_1", "value 1", "hint 1", "placeholder 1")
        return self

    def render(self):
        return {
                    "callback_id"      : self.callback_id     ,
                    "title"            : self.title           ,
                    "submit_label"     : self.submit_label    ,
                    "notify_on_cancel" : self.notify_on_cancel,
                    "elements"         : self.elements        }