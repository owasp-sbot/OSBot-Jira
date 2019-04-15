import unittest

from osbot_aws.apis.Lambda import Lambda

from osbot_jira.lambdas.jira import run

class test_lambda_gsbot_gs_jira(unittest.TestCase):

    def setUp(self):
        self.step_lambda   = Lambda('osbot_jira.lambdas.jira')

    # def test_lambda_update(self):
    #     self.step_lambda.update_with_lib()

    def test_invoke_directly(self):
        response = run({'data':{}},{})
        assert response[0] == '*Here are the `GS_Bot_Jira_Commands` commands available:*'


    def _send_command_message(self,command):
        payload = {'params' : [command] , 'data': {'team_id':'T7F3AUXGV', 'channel':'GDL2EC3EE'}}
        return self.step_lambda.invoke(payload)          # see answer in slack, or add a return to line 17 (in lambda_gs_bot)


    def test_invoke(self):
        response = self._send_command_message('help')
        assert response == [ ':red_circle: command not found `help`\n'
                              '\n'
                              '*Here are the `GS_Bot_Jira_Commands` commands available:*',
                              [ { 'actions': [],
                                  'callback_id': '',
                                  'color': 'good',
                                  'fallback': None,
                                  'text': ' • issue\n • projects\n • update\n'}]]
