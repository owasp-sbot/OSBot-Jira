import json
import  urllib
from    gs_jira.API_Jira_GS_CST import API_Jira_GS_CST
from    utils.Dev               import Dev

class Slash_Cst:
    def __init__(self):
        self.jira_cst = API_Jira_GS_CST().setup()

    def process_command(self, data):
        text      = data.get('text').replace('+',' ') # url decode wasn't working (this is a prob with the url encoded data provided by Slack
        commands  = text.split(" ")
        command   = commands.pop(0)
        if   command == 'projects': return self.cmd_projects()
        elif command == 'issue'   : return self.cmd_issue(commands)
        elif command == 'status'  : return self.cmd_status(commands)
        else                          : return "processing slash command for cst: {0}".format(text), []

    def cmd_issue(self, commands):
        attach = []
        if len(commands) == 0:
            text = ":red_circle: for the `issue` command you need to provide an valid Issue ID"
        else:
            key = commands.pop(0)
            issue       = self.jira_cst.jira.issue(key)
            transitions = self.jira_cst.jira.issue_next_transitions(key)
            issue_link = 'https://gs-cst.atlassian.net/browse/{0}'.format(key)
            text = '*<{0}|{1} - {2}>*'.format(issue_link,key,issue['Summary'])
            attach.append(
                {
                    "text"  : issue['Description'],
                    "fields": [
                                { "title": "Status"     , "value":     issue['Status'     ]  , "short": True },
                                { "title": "Labels"     , "value": str(issue['Labels'     ]) , "short": True },
                                { "title": "Creator"    , "value":     issue['Creator'    ]  , "short": True },
                                { "title": "Priority"   , "value":     issue['Priority'   ]  , "short": True },
                                { "title": "Issue Type" , "value":     issue['Issue Type' ]  , "short": True },
                                { "title": "Issue Links", "value": str(issue['Issue Links']) , "short": True }
                              ],
                    "color": "good"
                })
            subtasks = {"title": "Subtasks", "fields":[] }
            for key, subtask in issue['Subtasks'].items():
                subtask_link  = issue_link.format(key)
                subtask_text  = '<{0}|{1:10}> {2:12} {3:10} : *{4:10}*'.format(subtask_link          ,
                                                                             key                   ,
                                                                             subtask['Status'    ] ,
                                                                             subtask['Priority'  ] ,
                                                                             subtask['Summary'   ] )

                subtasks['fields'].append({'value': subtask_text , "color" : "good"})
            attach.append(subtasks)

            next_status  = {
                                "text": "Change Issue Status (from here):",
                                "callback_id": "change-issue-status",
                                "color": "#3AA3E3",
                                "actions": []}
            #for key,value in transitions.items():
            #    next_status['actions'].append({  "name": "next-status","text": key, "type": "button", "value": value })
            for status,status_id in transitions.items():
                value = json.dumps({ 'key': key, 'status': status, 'status_id': status_id }).replace('+',' ')
                next_status['actions'].append({  "name": 'next-status', "text": status, "type": "button", "value": value })

            attach.append(next_status)


        return text,attach

    def cmd_status(self, commands):
        attach = []
        if len(commands) == 0:
            text = ":red_circle: for the `issue` command you need to provide an valid Issue ID"
        else:
            key = commands.pop(0)
            issue       = self.jira_cst.jira.issue(key)
            transitions = self.jira_cst.jira.issue_next_transitions(key)
            issue_link = 'https://gs-cst.atlassian.net/browse/{0}'.format(key)
            text       = 'Current status of issue <{0}|{1} is *{2}*.\n\nWhat do you want to change it to?'.format(issue_link, key, issue.get('Status'))

            next_status  = {
                                "callback_id": "change-issue-status",
                                "color": "#3AA3E3",
                                "actions": []}
            for status,status_id in transitions.items():
                value = json.dumps({ 'key': key, 'status': status, 'status_id': status_id }).replace('+',' ')
                next_status['actions'].append({  "name": 'next-status', "text": status, "type": "button", "value": value })

            attach.append(next_status)
        return text,attach

    def cmd_projects(self):

        projects = self.jira_cst.jira.projects()

        attach_text = ""
        link_format = 'https://gs-cst.atlassian.net/projects/{0}'
        for key, project in projects.items():
            link = link_format.format(key)
            attach_text += '• <{0}|{1}>\n'.format(link, key, project.name)

        attach = [{ "text" : attach_text, "short": False}]
        text     = "*Here are the {0} projects found in the GS-CST server*".format(len(projects))
        return text, attach