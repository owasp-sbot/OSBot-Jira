from osbot_jira.api.gw.GW_Setup import load_dependency

def setup():
    load_dependency('jira')

def run(event, context):
    setup()
    from osbot_jira.api.jira_server.API_Jira import API_Jira

    server   = event.get('server')
    issue_id = event.get('issue_id')
    api_jira = API_Jira().set_public_jira(server)
    issue = api_jira.issue(issue_id)
    return issue