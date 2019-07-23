from osbot_aws.apis.Lambdas import Lambdas


def run(event, context):
    request_test = Lambda('dev.node_phantom')

    if event.get('width') is None:
        event['width'] = 1000
    return request_test.invoke(event)
