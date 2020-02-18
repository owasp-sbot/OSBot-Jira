from osbot_aws.Dependencies import load_dependency


def run(event, context):
    load_dependency('gmail') ;
    from _from_pydot.gmail.API_GMail import API_GMail
    gmail = API_GMail().setup()
    return gmail.labels()