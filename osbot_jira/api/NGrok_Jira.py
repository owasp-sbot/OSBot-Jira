import requests
from osbot_aws.apis.Secrets import Secrets

from pbx_gs_python_utils.utils.Misc import Misc


class NGrok_Jira:
    def __init__(self):
        self.ngrok_url = 'https://gs-jira.ngrok.io'
        self._secrets  = None

    # helper methods
    def secrets(self):
        if self._secrets is None:
            data = Secrets('sync-server-ngrok').value_from_json_string()
            username = data.get('username')
            password = data.get('password')
            self._secrets = (username,password)
        return self._secrets

    # command = 'gsbot_jira/invoke/{"params":["projects"]}'
    # command = 'gsbot_jira/invoke/{"params":["issue","AAA-42"]}'
    def invoke(self,method):
        username,password = self.secrets()
        command = 'gsbot_jira'
        url = "{0}/{1}/{2}".format(self.ngrok_url,command, method)
        return Misc.json_load(requests.get(url, auth=(username, password)).text)

    # main api methods

    def issue(self,issue_id):
        return self.invoke('issue/{0}'.format(issue_id))

    def update(self,issue_id,field,value):
        return self.invoke('update/{0}/{1}/{2}'.format(issue_id, field, value))

    def projects(self):
        return self.invoke('invoke/{"params":["projects"]}')

    def version(self):
        return self.invoke('version')