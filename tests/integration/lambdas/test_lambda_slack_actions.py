import unittest
from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment

class test_lambda_gsbot_gs_jira(TestCase):

    def setUp(self):
        self.aws_lambda = Lambda('osbot_jira.lambdas.slack_actions')
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_lambda_update(self):
        Lambda_Package('osbot_jira.lambdas.slack_actions').update_code()

    # def test_invoke_directly(self):
    #     response = run({'data':{}},{})
    #     assert response[0] == '*Here are the `GS_Bot_Jira_Commands` commands available:*'



    def test_invoke(self):
        self.test_lambda_update()
        self.result = self.aws_lambda.invoke({})



    def test__create_button_to_test_dialog(self):
        self.test_lambda_update()
        self.api_attach = API_Slack_Attachment()
        self.api_attach.set_text       ('Click on button below to test dialog'          )   \
                       .set_callback_id("gs_detect_slack"                            )   \
                       .add_button     ("button 1", "gs detect test", "open 1", "primary"   )
        attachments = self.api_attach.render()

        slack_message("one message", attachments, 'DJYDAS51B')

    def test_invoke__with_test_button_click_event(self):
        self.test_lambda_update()
        payload = {'type': 'interactive_message', 'actions': [{'name': 'button+1', 'type': 'button', 'value': 'open+1'}], 'callback_id': 'button-dialog-test', 'team': {'id': 'T7F3AUXGV', 'domain': 'gs-cst'}, 'channel': {'id': 'DDKUZTK6X', 'name': 'directmessage'}, 'user': {'id': 'U7ESE1XS7', 'name': 'dinis.cruz'}, 'action_ts': '1560853130.127802', 'message_ts': '1560853127.000500', 'attachment_id': '1', 'token': 'a2J5DIEEJZtKOSZHZBqgDnVz', 'is_app_unfurl': False, 'original_message': {'type': 'message', 'subtype': 'bot_message', 'text': 'one+message', 'ts': '1560853127.000500', 'username': 'gs-bot', 'bot_id': 'BDKLUMX4K', 'attachments': [{'callback_id': 'button-dialog-test', 'fallback': 'Click+on+button+below+to+test+dialog', 'text': 'Click+on+button+below+to+test+dialog', 'id': 1, 'color': '3AA3E3', 'actions': [{'id': '1', 'name': 'button+1', 'text': 'click-me-1', 'type': 'button', 'value': 'open+1', 'style': 'primary'}, {'id': '2', 'name': 'button+2', 'text': 'click-me-2', 'type': 'button', 'value': 'open+2', 'style': 'primary'}]}]}, 'response_url': 'https://hooks.slack.com/actions/T7F3AUXGV/668389575413/fa9NGk6KvGPe8d9io9n2eTmc', 'trigger_id': '656981015107.253112983573.a337fcceabba9cd21113700e39b41423'}
        self.result = self.aws_lambda.invoke(payload)

    def test_invoke__with_fialog_submission(self):
        self.test_lambda_update()
        payload = {'type': 'dialog_submission', 'token': 'a2J5DIEEJZtKOSZHZBqgDnVz', 'action_ts': '1560886997.880872', 'team': {'id': 'T7F3AUXGV', 'domain': 'gs-cst'}, 'user': {'id': 'U7ESE1XS7', 'name': 'dinis.cruz'}, 'channel': {'id': 'DDKUZTK6X', 'name': 'directmessage'}, 'submission': {'summary': 'an+summary+1'}, 'callback_id': 'issue-suggestion', 'response_url': 'https://hooks.slack.com/app/T7F3AUXGV/671229078598/xKLbB0wSefs2ZlVSqrdKftpB', 'state': ''}
        self.result = self.aws_lambda.invoke(payload)



    def test_send_menu(self):
        text = 'an dynamic menu'
        attachments =  [
                            {
                                "fallback": "Upgrade your Slack client to use messages like these.",
                                "color": "3AA3E3",
                                "attachment_type": "default",
                                "callback_id": "select_remote_1234",
                                "actions": [
                                    {
                                        "name": "bugs_list",
                                        "text": "Which random bug do you want to resolve?",
                                        "type": "select",
                                        "data_source": "external",
                                        "min_query_length": 1,
                                    }
                                ]
                            }
                        ]
        self.test_lambda_update()
        slack_message("one message", attachments, 'DDKUZTK6X')