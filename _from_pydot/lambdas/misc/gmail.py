from utils.aws.Lambdas import load_dependency


def run(event, context):
    load_dependency('gmail') ; from API_GMail import API_GMail
    gmail = API_GMail().setup()
    return gmail.labels()