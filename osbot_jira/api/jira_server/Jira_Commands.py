# These are the methods to be called inside the Sync Server
import json

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.api.jira_server.API_Jira import API_Jira


class Jira_Commands:

    gsbot_projects = ['GSBOT','IA','SEC','RISK','VULN']

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

    @staticmethod
    def authorized_project(project):
        return project in Jira_Commands.gsbot_projects

    @staticmethod
    def projects(team_id=None, channel=None, params=None):
        return Jira_Commands.gsbot_projects

    @staticmethod
    def issue(team_id=None, channel=None, params=None):
        (text, attachments) = Jira_Commands._check_params(params, ['Issue Id'])
        if text: return text#, attachments

        issue_id,  = params
        project = issue_id.split('-').pop(0)
        projects = Jira_Commands.gsbot_projects
        if project not in projects:
            return {"error" : ":rec_circle: project `{0}` is currently not available. The projects currently supported are: `{1}`".format(project,projects) }

        return API_Jira().issue(issue_id)

    @staticmethod
    def update(team_id=None, channel=None, params=None):
        try:

            issue_data = json.loads(" ".join(params))
            issue_id   = issue_data.get('Key')
            project = issue_id.split('-').pop(0)
            projects = Jira_Commands.gsbot_projects
            if project not in projects:
                return ":rec_circle: project `{0}` is currently not available. The projects currently supported are: `{1}`".format(
                    project, projects)

            API_Jira().issue_update(issue_data)
            return { "status" : "ok" }
        except Exception as error:
            return {"error",":rec_circle: error in `Jira_Commands.update` command: `{0}`".format(error)}

    @staticmethod
    def version(team_id=None, channel=None, params=None):
        return "0.11.6"
