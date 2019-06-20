from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.Deploy import Deploy
from osbot_jira.api.slack.Slack_Dialog_Submissions import Slack_Dialog_Submissions


class test_Slack_Dialog_Submissions(TestCase):

    def setUp(self):
        self.submission       = {'channel': 'DDKUZTK6X'}
        self.dialog_submissions = Slack_Dialog_Submissions(self.submission)
        self.result = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_handle(self):
        self.result = self.dialog_submissions.handle()


    def test__update_lambda(self):
        Deploy('osbot_jira.lambdas.slack_jira_actions').deploy()  # update the jira actions

