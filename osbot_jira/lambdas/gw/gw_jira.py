from osbot_jira.api.gw.GW_Setup import load_dependency

# def setup():
#     load_dependency('jira')
#
# def run(event, context):
#     setup()
#
#     server   = event.get('server')
#     issue_id = event.get('issue_id')
#
#     from osbot_jira.api.jira_server.API_Jira import API_Jira
#     api_jira = API_Jira().set_public_jira(server)
#     return  api_jira.issue(issue_id)

def setup():
    load_dependency('requests')

def run(event, context):
    setup()

    server   = event.get('server')
    issue_id = event.get('issue_id')

    from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
    api_jira_rest = API_Jira_Rest().set_public_jira(server)

    return api_jira_rest.issue(issue_id)