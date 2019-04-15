from pbx_gs_python_utils.utils.Lambdas_Helpers import log_to_elk
from osbot_aws.apis.Lambda import load_dependency


def run(event, context):
    try:
        load_dependency("elastic")
        from osbot_jira.api.elk.Elk_To_Slack import ELK_to_Slack
        return ELK_to_Slack().handle_lambda_event(event)
    except Exception as error:
        log_to_elk("[elk_to_slack][Error]: {0}".format(error) , level='error')
