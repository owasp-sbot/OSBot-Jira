from osbot_aws.Dependencies import load_dependency
from osbot_aws.helpers.Lambda_Helpers import log_to_elk


def run(event, context):
    try:
        load_dependency("elastic")
        from osbot_jira.api.elk.Elk_To_Slack import ELK_to_Slack
        return ELK_to_Slack().handle_lambda_event(event)
    except Exception as error:
        log_to_elk("[elk_to_slack][Error]: {0}".format(error) , level='error')
