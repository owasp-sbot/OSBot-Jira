from pbx_gs_python_utils.utils.slack.API_Slack_Dialog import API_Slack_Dialog


class Jira_Create_Issue(API_Slack_Dialog):

    def __init__(self, project='SEC', issue_type='Task', summary='New issue', description=''):
        self.project = project
        self.issue_type = issue_type
        self.description = description
        self.summary = summary
        super().__init__()

    def setup(self):
        self.callback_id = 'jira_create_issue'
        self.title       = 'Create new issue in JIRA'
        self.add_element_select  ("Project", 'project', [('SEC','SEC'),('VULN','VULN'),('RISK','RISK'),('GSCS','GSCS')],value=self.project)
        self.add_element_select  ("Issue Type", 'issue_type', [('Task','Task'),('Meeting','Meeting'),('Vulnerability','Vulnerability'),('Risk','Risk')], value=self.issue_type)
        self.add_element_text    ("Summary", "summary", value=self.summary, optional= False , hint="This is the issue's summary")
        self.add_element_textarea("Description", "description",value=self.description, optional= True)

        return self

    def render(self):
        return {
                    "callback_id"      : self.callback_id     ,
                    "title"            : self.title           ,
                    "submit_label"     : self.submit_label    ,
                    "notify_on_cancel" : self.notify_on_cancel,
                    "elements"         : self.elements        }