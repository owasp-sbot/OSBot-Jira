# not working (could be token related)
# from unittest import TestCase
#
# from osbot_utils.utils.Dev import Dev
#
#
# class test_Jira_Edit_Field(TestCase):
#
#     def setUp(self):
#         self.trigger_id = '692211281543.253112983573.eb600292b78df308bb804723844d1ad2' # short lived token
#         self.result     = None
#
#     def tearDown(self):
#         if self.result is not None:
#             Dev.pprint(self.result)
#
#
#     def test_open_ui(self):
#         from osbot_jira.api.slack.dialogs.Jira_Create_Issue import Jira_Create_Issue
#         from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
#
#         slack_dialog = Jira_Create_Issue().setup().render()
#         self.result = API_Slack().slack.api_call("dialog.open", trigger_id=self.trigger_id, dialog=slack_dialog)
