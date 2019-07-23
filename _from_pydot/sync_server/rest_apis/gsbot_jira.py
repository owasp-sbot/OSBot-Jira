from flask_restplus import Namespace, Resource
from osbot_jira.api.jira_server.API_Jira import API_Jira
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

api                = Namespace('gsbot_jira', description='GSBot Jira API')
jira_api           = API_Jira()
gsbot_jira_version = 'v0.10.6'
gsbot_projects     = ['GSBOT','IA','SEC','RISK','VULN']

# @api.route('/invoke/<payload>')         # change this to be a post method
# class invoke(Resource):
#     def get(self,payload):
#         try:
#             data = json.loads(payload)
#             team_id = data.get('team_id')
#             channel = data.get('channel')
#             params  = data.get('params')
#             text,_ = Slack_Commands_Helper(Jira_Commands).invoke(team_id, channel, params)
#             return text
#         except Exception as error:
#             return {"error": "{0}".format(error)}

from functools import wraps

def send_slack_message(message):
    slack_message(str(message),[],'GH4L1N6PN', 'T7F3AUXGV')  # send logs to gsbot-logs-gs-jira

def log_message(message):
    send_slack_message(':point_right: ' + str(message))
    return message

def ok_message(message):
    send_slack_message(':point_right: ' + str(message))
    return {"message": message, "status":"ok"    ,"code":201 }

def ok_result(data):
    return {"result": data, "status":"ok"    ,"code":202 }

def error_message(message):
    send_slack_message(':red_circle: ' + str(message))
    return {"message": message, "status": "error", "code": 501}


def error_project_not_supported():
    return error_message("Project not currently supported. Here are the projects currently available via GSBot: `{0}`".format(gsbot_projects))


#todo: add way to check if JIRA server is available (create ticket)
def authorize_request(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        try:
            # print()
            # print( len(args),len(kwds))
            # if len(args) != len(kwds):
            #     return error_message("GSBot internal error: args and kwds lens don't match")
            # print()
            #fields = inspect.getfullargspec(func).args
            issue_id = kwds.get('issue_id')
            project  = kwds.get('project')
            if issue_id:
                project = issue_id.split('-').pop(0)
                if project not in gsbot_projects:
                    return error_project_not_supported()

            if project:
                if project not in gsbot_projects:
                    return error_project_not_supported()

            kwds['jira'] = jira_api
            return func(*args, **kwds)
        except Exception as error:
            return error_message(("GSBot internal error: in authorize request wrapper: {0}".format(error)))


    return wrapper




@api.route('/projects')
class projects(Resource):
    def get(self):
        return gsbot_projects
        #params = ['projects']
        #text, _ = Slack_Commands_Helper(Jira_Commands).invoke(None, None, params)
        #return text


@api.route('/create_issue/<project>/<issue_type>/<summary>/<description>')
class create_issue(Resource):
    @authorize_request
    def get(self, project, issue_type, summary,description,jira):
        return jira.issue_create(project, summary, description, issue_type)


@api.route('/issue/<issue_id>')
class issue(Resource):

    @authorize_request
    def get(self,issue_id,jira):
        ok_message("issue(`{0}`)".format(issue_id))
        return ok_result(jira.issue(issue_id))
        # project = issue_id.split('-').pop(0)
        # if project in gsbot_projects:
        #     return jira_api.issue(issue_id)
        # return {"error": "Project not currently supported"}

@api.route('/update/<issue_id>/<field>/<value>')
class update(Resource):
    @authorize_request
    def get(self,issue_id, field, value,jira):
        issue_data = {"Key": issue_id, field:value}
        jira.issue_update(issue_data)
        return ok_result('update request sent')


@api.route('/version')
class version(Resource):
    def get(self):
        return {  'gsbot_jira': gsbot_jira_version }
