from osbot_aws.apis.Lambda import load_dependencies

def run(event, context):
    try:
        load_dependencies(["elastic-slack",'requests'])                     # load dependency (download and unzip if first run)
        from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph          # import Lambda_Graph class
        return Lambda_Graph().handle_lambda_event(event)                    # invoke lambda handler from Lambda_Graph class
    except Exception as error:
        return ":red_circle: error in `osbot_jira.lambdas.graph`: {0}".format(error)