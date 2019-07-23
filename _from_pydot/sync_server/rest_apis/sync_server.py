import os

from flask_restplus                         import Namespace, Resource
from osbot_jira.api.jira_server.API_Jira import API_Jira
from pbx_gs_python_utils.utils.Http         import GET

api      = Namespace('server', description='JIRA issues related operations')
jira_api = API_Jira()

@api.route('/docker_env')
class status(Resource):
    def get(self):
        return { 'value': os.getenv('SYNC_SERVER') }

@api.route('/status')
class status(Resource):
    def get(self):
        return { 'status': 'OK 12345' }

@api.route('/version')
class version(Resource):
    def get(self):
        return { 'version': 'v0.65.1' }


@api.route('/reload')
class reload(Resource):
    def get(self):
        result = GET('http://127.0.0.1:21112')
        return { 'status': result }

