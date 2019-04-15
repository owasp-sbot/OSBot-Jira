# These are the methods to be called by Slack
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jira.api.NGrok_Jira import NGrok_Jira


class GS_Bot_Jira_Commands:

    @staticmethod
    def _check_params(params, expected_params):
        if len(params) != len(expected_params):
            text = ':red_circle: For this command, you need to provide the following parameters: '
            attachment_text = ''
            for expected_param in expected_params:
                attachment_text += '- {0} \n'.format(expected_param)
            attachments = [{'text': attachment_text}]
            return text, attachments
        return None, None

    # main methods
    @staticmethod
    def projects(team_id=None, channel=None, params=None):
        projects = NGrok_Jira().projects()
        return ":point_right: Here are the projects that GSBot currently supports: `{0}`".format(projects)

    @staticmethod
    def issue(team_id=None, channel=None, params=None):
        (text, attachments) = GS_Bot_Jira_Commands._check_params(params, ['Issue Id'])
        if text: return text, attachments
        issue_id = params.pop(0)
        issue = NGrok_Jira().issue(issue_id)
        return ":point_right: Issue `{0}` details\n```{1}```".format(issue_id,  Misc.json_format(issue))

    @staticmethod
    def update(team_id=None, channel=None, params=None):
        #(text, attachments) = GS_Bot_Jira_Commands._check_params(params, ['Issue Id'])
        issue_id = Misc.array_pop_and_trim(params,0)
        command = ' '.join(params)
        items   = command.split('=')
        field   = Misc.array_pop_and_trim(items,0)
        value   = Misc.trim(''.join(items))
        print()
        print(issue_id)
        print(command)
        print(field)
        print(value)
        if issue_id and field and value:
            return NGrok_Jira().update(issue_id,field,value)

        return ':red_circle: Incorrect values provided for `update` command. The syntax is {issue_id} {field}={value}'



