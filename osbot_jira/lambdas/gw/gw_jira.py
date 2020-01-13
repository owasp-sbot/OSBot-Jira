from osbot_jira.api.gw.GW_Setup import load_dependency

def setup():
    load_dependency('jira')

def run2(event, context):
    setup()

    issue_id = event.get('issue_id')

    from osbot_jira.api.jira_server.API_Jira import API_Jira
    api_jira = API_Jira()
    data = api_jira.issue(issue_id)
    return data



def run(event, context):
    setup()

    server   = event.get('server')
    issue_id = event.get('issue_id')

    from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
    api_jira_rest = API_Jira_Rest()

    return api_jira_rest.issue(issue_id)