from gw_bot.Deploy import Deploy
from gw_bot.api.slack.API_Slack_Attachment import API_Slack_Attachment
from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_aws.apis.Lambda import Lambda
from osbot_utils.utils.Dev import Dev
from osbot_aws.helpers.Lambda_Helpers import slack_message
from osbot_jira.lambdas.slack_actions import run


class test_lambda_gsbot_gs_jira(Test_Helper):

    def setUp(self):
        super().setUp()
        self.aws_lambda = Lambda('osbot_jira.lambdas.slack_actions')

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_lambda_update(self):
        Deploy().deploy_lambda__jira('osbot_jira.lambdas.slack_actions')

    def test_invoke_directly_with_payload(self):
        payload = {'type': 'block_actions', 'team': {'id': 'TRQU3V52S', 'domain': 'glasswall-solutions'}, 'user': {'id': 'UR9UENEAW', 'username': 'dcruz', 'name': 'dcruz', 'team_id': 'TRQU3V52S'}, 'api_app_id': 'ARQD319T7', 'token': 'grIGwKiaF1AYTrgpfyLYwsI2', 'container': {'type': 'message', 'message_ts': '1582152217.035800', 'channel_id': 'DRE51D4EM', 'is_ephemeral': False}, 'trigger_id': '947439811026.874955991094.568da2433c5af94ab19c4dbe3c885cdb', 'channel': {'id': 'DRE51D4EM', 'name': 'directmessage'}, 'message': {'type': 'message', 'subtype': 'bot_message', 'text': "This+content+can't+be+displayed.", 'ts': '1582152217.035800', 'username': 'GW-Bot', 'bot_id': 'BRCUGDR4K', 'blocks': [{'type': 'section', 'block_id': 'block_YT2N', 'text': {'type': 'mrkdwn', 'text': ':point_right:+*Issue*:+<bcf66c78613e430c99ee866a98d31262.eu-west-1.aws.found.io/browse/TASK-60|TASK-60+-+a+new+test>', 'verbatim': False}}, {'type': 'section', 'block_id': 'block_W0QX', 'text': {'type': 'mrkdwn', 'text': '*Change+issue+status+to*:+(click+to+change)', 'verbatim': False}}, {'type': 'actions', 'block_id': 'block_OUEA', 'elements': [{'type': 'button', 'action_id': 'class_method::Jira_View_Issue::transition_to::21', 'text': {'type': 'plain_text', 'text': 'Ready+For+Review', 'emoji': True}, 'value': 'TASK-60::21::Ready+For+Review'}, {'type': 'button', 'action_id': 'class_method::Jira_View_Issue::transition_to::111', 'text': {'type': 'plain_text', 'text': 'Stop+Progress', 'emoji': True}, 'value': 'TASK-60::111::Stop+Progress'}, {'type': 'button', 'action_id': 'class_method::Jira_View_Issue::transition_to::151', 'text': {'type': 'plain_text', 'text': 'Done', 'emoji': True}, 'value': 'TASK-60::151::Done'}]}, {'type': 'section', 'block_id': 'block_GW9G', 'text': {'type': 'mrkdwn', 'text': '*Edit+Issue+Field:*+(select+to+edit)', 'verbatim': False}}, {'type': 'actions', 'block_id': 'block_VJOA', 'elements': [{'type': 'static_select', 'action_id': 'class_method::Jira_View_Issue::edit_field::TASK-60::field_to_edit', 'placeholder': {'type': 'plain_text', 'text': 'Field+to+edit', 'emoji': True}, 'options': [{'text': {'type': 'plain_text', 'text': 'Assignee', 'emoji': True}, 'value': 'Assignee'}, {'text': {'type': 'plain_text', 'text': 'Description', 'emoji': True}, 'value': 'Description'}, {'text': {'type': 'plain_text', 'text': 'Labels', 'emoji': True}, 'value': 'Labels'}, {'text': {'type': 'plain_text', 'text': 'Latest+Information', 'emoji': True}, 'value': 'Latest+Information'}, {'text': {'type': 'plain_text', 'text': 'Summary', 'emoji': True}, 'value': 'Summary'}]}]}, {'type': 'section', 'block_id': 'block_2B48', 'text': {'type': 'mrkdwn', 'text': '*Actions*', 'verbatim': False}}, {'type': 'actions', 'block_id': 'block_C5Q7', 'elements': [{'type': 'button', 'action_id': 'class_method::Jira_View_Issue::view_links', 'text': {'type': 'plain_text', 'text': 'View+Links', 'emoji': True}, 'value': 'TASK-60'}, {'type': 'button', 'action_id': 'class_method::Jira_View_Issue::screenshot', 'text': {'type': 'plain_text', 'text': 'Screenshot', 'emoji': True}, 'value': 'TASK-60'}, {'type': 'button', 'action_id': 'class_method::Jira_View_Issue::reload_issue', 'text': {'type': 'plain_text', 'text': 'Reload+Issue', 'emoji': True}, 'value': 'TASK-60'}, {'type': 'button', 'action_id': 'class_method::Jira_View_Issue::raw_issue_data', 'text': {'type': 'plain_text', 'text': 'Raw+Issue+Data', 'emoji': True}, 'value': 'TASK-60'}]}, {'type': 'divider', 'block_id': 'ziFZ'}, {'type': 'context', 'block_id': 'block_XKN0', 'elements': [{'type': 'mrkdwn', 'text': 'Rating:+None', 'verbatim': False}, {'type': 'mrkdwn', 'text': 'Priority:+Medium', 'verbatim': False}, {'type': 'mrkdwn', 'text': 'Issue+Type:+Task', 'verbatim': False}, {'type': 'mrkdwn', 'text': 'Assignee:+None', 'verbatim': False}, {'type': 'mrkdwn', 'text': 'Labels:+None', 'verbatim': False}, {'type': 'mrkdwn', 'text': 'Creator:+None', 'verbatim': False}, {'type': 'mrkdwn', 'text': 'Created:+2020-02-19', 'verbatim': False}, {'type': 'mrkdwn', 'text': 'Updated:+2020-02-19', 'verbatim': False}]}]}, 'response_url': 'https://hooks.slack.com/actions/TRQU3V52S/962437095158/MQrgn7uTq1VIKcu4PJtqVEe4', 'actions': [{'type': 'static_select', 'action_id': 'class_method::Jira_View_Issue::edit_field::TASK-60::field_to_edit', 'block_id': 'block_VJOA', 'selected_option': {'text': {'type': 'plain_text', 'text': 'Description', 'emoji': True}, 'value': 'Description'}, 'placeholder': {'type': 'plain_text', 'text': 'Field+to+edit', 'emoji': True}, 'action_ts': '1582152400.262464'}]}
        payload = {'type': 'dialog_submission', 'token': 'grIGwKiaF1AYTrgpfyLYwsI2', 'action_ts': '1582153511.343061', 'team': {'id': 'TRQU3V52S', 'domain': 'glasswall-solutions'}, 'user': {'id': 'UR9UENEAW', 'name': 'dcruz'}, 'channel': {'id': 'DRE51D4EM', 'name': 'directmessage'}, 'submission': {'TASK-60::Summary': 'a+new+testAAAAAAAAAA'}, 'callback_id': 'jira_edit_issue', 'response_url': 'https://hooks.slack.com/app/TRQU3V52S/950128493681/PvzySbviprciuHfLJFFZN8jJ', 'state': ''}
        payload = {'type': 'interactive_message', 'actions': [{'name': 'jira-actions', 'type': 'button', 'value': 'create_issue'}], 'callback_id': 'jira-slack-actions', 'team': {'id': 'TRQU3V52S', 'domain': 'glasswall-solutions'}, 'channel': {'id': 'DRE51D4EM', 'name': 'directmessage'}, 'user': {'id': 'UR9UENEAW', 'name': 'dcruz'}, 'action_ts': '1582155752.564879', 'message_ts': '1582155697.059500', 'attachment_id': '1', 'token': 'grIGwKiaF1AYTrgpfyLYwsI2', 'is_app_unfurl': False, 'original_message': {'type': 'message', 'subtype': 'bot_message', 'text': ':point_right:+Hello,+here+are+the+currently+supported+Jira+Actions', 'ts': '1582155697.059500', 'username': 'GW-Bot', 'bot_id': 'BRCUGDR4K', 'attachments': [{'callback_id': 'jira-slack-actions', 'id': 1, 'color': '3AA3E3', 'actions': [{'id': '1', 'name': 'jira-actions', 'text': 'Create+Issue', 'type': 'button', 'value': 'create_issue', 'style': 'primary'}, {'id': '2', 'name': 'jira-actions', 'text': 'Search', 'type': 'button', 'value': 'search', 'style': 'primary'}], 'fallback': '[no+preview+available]'}]}, 'response_url': 'https://hooks.slack.com/actions/TRQU3V52S/950172142897/d5qEaWKzMBewqWy49jgxtHsJ', 'trigger_id': '948828513811.874955991094.118063096d956be1d8f0dbef30b9b046'}
        self.result = run(payload)

    #     assert response[0] == '*Here are the `GS_Bot_Jira_Commands` commands available:*'



    def test_invoke(self):
        self.test_lambda_update()
        self.result = self.aws_lambda.invoke({})



    def test__create_button_to_test_dialog(self):
        self.test_lambda_update()
        self.api_attach = API_Slack_Attachment()
        self.api_attach.set_text       ('Click on button below to test dialog'          ) \
            .set_callback_id("gs_detect_slack"                            ) \
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