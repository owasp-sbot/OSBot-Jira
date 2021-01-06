# from unittest import TestCase
#
# from osbot_utils.utils.Dev import Dev
#
# from osbot_jira.api.GS_Bot_Jira_Commands import GS_Bot_Jira_Commands

#NOT Used
# class Test_GS_Bot_Jira_Commands(TestCase):
#
#     def setUp(self):
#         self.jira_commands = GS_Bot_Jira_Commands()
#
#     def test_projects(self):
#         assert self.jira_commands.projects() == ':point_right: Here are the projects that GSBot currently supports: `None`'
#
#     def test_issue(self):
#         params = ['RISK-42']
#         result = self.jira_commands.issue(params=params)
#         Dev.pprint(result)
#
#     def test_update(self):
#         params = ['RISK-42  ','Summary = ',' From GSBot Jira Commands test = 123']
#         result = self.jira_commands.update(params=params)
#         Dev.pprint(result)