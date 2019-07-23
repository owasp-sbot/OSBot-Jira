import unittest
from unittest import TestCase

from osbot_aws.helpers.Lambda_Package import Lambda_Package
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

from osbot_jira.Deploy import Deploy


class test_Deploy_Lambda_Functions(TestCase):

    def test_deploy_lambda_functions(self):
        #code_path = Files.path_combine('.','..')

        targets = [
                    'osbot_jira.lambdas.elastic_jira'    ,   #   elastic_jira.py    GS_Bot_Jira
                    #'osbot_jira.lambdas.jira'            ,   #   jira.py            GS_Bot_Jira_Commands
                    'osbot_jira.lambdas.graph'           ,   #   graph.py

                   ]
        result = ""
        for target in targets:
            Deploy(target).deploy()
            result += " • {0}\n".format(target)

        text        = ":hotsprings: [osbot-gsuite] updated lambda functions"
        attachments = [{'text': result, 'color': 'good'}]
        slack_message(text, attachments)  # gs-bot-tests
        Dev.pprint(text, attachments)

    #def test_deploy_jira(self):
    #    Lambda_Package('osbot_jira.lambdas.jira').update_code()

    # lambda called when using the @osbot jira command
    def test_deploy_elastic_jira(self):
        Lambda_Package('osbot_jira.lambdas.elastic_jira').update_code() #  GS_Bot_Jira

    def test_deploy_slack_actions(self):
        Lambda_Package('osbot_jira.lambdas.slack_actions').update_code() #  GS_Bot_Jira

    def test__update_lambda(self):
        Deploy('osbot_jira.lambdas.slack_jira_actions').deploy()  # update the jira actions

if __name__ == '__main__':
    unittest.main()