from flask_restplus                        import Namespace, Resource
from osbot_jira.api.jira_server.API_Jira import API_Jira

api      = Namespace('jira-sync', description='JIRA issues related operations')
jira_api = API_Jira()

@api.route('/load-jira/<file_id>')
class load_jira(Resource):
    def get(self, file_id):
        try:
            from pbx_gs_python_utils.api_jira.API_Jira_Sheets_Sync import API_Jira_Sheets_Sync
            api_sync = API_Jira_Sheets_Sync(file_id)
            result = api_sync.load_data_from_jira()
            return { 'status': result }
        except Exception as error:
            return { 'error' : "{0}".format(error)}

@api.route('/diff-sheet/<file_id>')
class diff_sheet(Resource):
    def get(self, file_id):
        try:
            from pbx_gs_python_utils.api_jira.API_Jira_Sheets_Sync import API_Jira_Sheets_Sync
            api_sync = API_Jira_Sheets_Sync(file_id)
            result = api_sync.diff_sheet()
            return { 'status': result }
        except Exception as error:
            return { 'error' : "{0}".format(error)}


@api.route('/sync-sheet/<file_id>')
class sync_sheet(Resource):
    def get(self, file_id):
        try:
            from pbx_gs_python_utils.api_jira.API_Jira_Sheets_Sync import API_Jira_Sheets_Sync
            api_sync = API_Jira_Sheets_Sync(file_id)
            result = api_sync.sync_sheet()
            return { 'status': result }
        except Exception as error:
            return { 'error' : "{0}".format(error)}

@api.route('/sheet-from-graph/<graph_name>')
class sheet_from_graph(Resource):
    def get(self,graph_name):
        try:
            folder = '1o-kpQ9sLzo0_wE13XcmnUuH7GNsHpdbp'  # for now hard code these
            domain = 'photobox.com'
            from pbx_gs_python_utils.api_jira.API_Jira_Sheets_Sync import API_Jira_Sheets_Sync
            api_sync = API_Jira_Sheets_Sync()
            result = api_sync.create_sheet_from_graph(graph_name,domain,folder)
            return { 'status': result }
        except Exception as error:
            return { 'error' : "{0}".format(error)}


@api.route('/version')
class version(Resource):
    def get(self):
        return 'v0.22'