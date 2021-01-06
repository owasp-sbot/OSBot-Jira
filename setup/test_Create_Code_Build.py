from time                                import sleep
from unittest                            import TestCase
from osbot_aws.helpers.Create_Code_Build import Create_Code_Build


class test_Create_Code_Build(TestCase):

    def setUp(self):
        self.project_name    = 'OSBot-jira'
        self.api             = Create_Code_Build(project_name=self.project_name)

    def test_create(self):
        policies = self.api.policies__with_ecr_and_3_secrets()
        self.api.create_role_and_policies(policies)
        sleep(5)                                                        # to give time for AWS to sync up internally
        self.api.create_project_with_container__gs_docker_codebuild()
        self.api.code_build.build_start()

