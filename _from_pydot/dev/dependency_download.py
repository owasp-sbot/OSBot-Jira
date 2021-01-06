from osbot_aws.Dependencies import load_dependency

def run(event, context):
    load_dependency("slack")                                                # this will download the dependencies the first time the lambda function is executed

    from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
    API_Slack(channel='...').send_message("this was sent from an lambda function")

    #load_dependency("requests")                                             # the Slack dependency already includes this dependency
    import requests
    return len(requests.get("https://www.google.com").text)