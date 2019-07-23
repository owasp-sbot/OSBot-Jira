
from osbot_aws.apis.Lambda import load_dependency


def run(event, context):
    load_dependency('elastic')
    from gs.API_Elastic_Lambda import API_Elastic_Lambda
    return API_Elastic_Lambda().handle_lambda_event(event)