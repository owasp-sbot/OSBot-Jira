from flask_restplus                        import Namespace, Resource
from osbot_jira.api.jira_server.API_Jira   import API_Jira

from API_Elastic_Jira                      import API_Elastic_Jira

api      = Namespace('jira', description='JIRA issues related operations')
jira_api = API_Jira()

# @api.route('/jira-web-hook')
# class jira_update_hook(Resource):
#     def post(self):
#         index        = 'jira'
#         projects     = 'VULN,RISK,FACT'
#         elastic_jira = API_Elastic_Jira(index, projects).setup()
#         elastic_jira.update_index_from_jira_changes()
#         return { 'action': 'updating projects {0}'.format(projects) }
#
# @api.route('/jira-web-hook-sec')
# class jira_update_hook_sec(Resource):
#     def post(self):
#         index        = 'sec_project'
#         projects     = 'SEC'
#         elastic_jira = API_Elastic_Jira(index, projects).setup()
#         elastic_jira.update_index_from_jira_changes()
#         return { 'action': 'updating projects {0}'.format(projects) }
#
# @api.route('/jira-web-hook-ia')
# class jira_update_hook_ia(Resource):
#     def post(self):
#         index        = 'it_assets'
#         projects     = 'IA,TM,GSP,GSOKR,RT,FIX,SC,GSSP,SL,GSOS,GSCS,GSBOT'
#         elastic_jira = API_Elastic_Jira(index, projects).setup()
#         elastic_jira.update_index_from_jira_changes()
#         return { 'action': 'updating projects {0}'.format(projects) }
#
# @api.route('/reload-elk-index-jira')
# class reload_elk_index_jira(Resource):
#     def post(self):
#         return API_Elastic_Jira().setup().reload_jira_index__jira()
#
# @api.route('/reload-elk-index-sec')
# class reload_elk_index_sec(Resource):
#     def post(self):
#         return API_Elastic_Jira().setup().reload_jira_index__sec_project()
#
# @api.route('/reload-elk-index-it-assets')
# class reload_elk_index_it_assets(Resource):
#     def post(self):
#         return API_Elastic_Jira().setup().reload_jira_index__it_Assets()
#
# @api.route('/reload-elk-indexes')
# class reload_elk_indexes(Resource):
#     def post(self):
#         result = {
#                     "jira"       : API_Elastic_Jira().setup().reload_jira_index__jira()         ,
#                     "it_assets"  : API_Elastic_Jira().setup().reload_jira_index__it_Assets()    ,
#                     "sec_project": API_Elastic_Jira().setup().reload_jira_index__sec_project()
#                  }
#         return result





# @api.route('/reload-jira-index-data')
# class jira_reload_jira_index_data(Resource):
#     def get(self):
#         return 42
#
# @api.route('/get/<id>')
# class list_issues(Resource):
#     def get(self, id):
#         return jira_api.issue(id)
#
# @api.route('/projectsAAAA')
# class projects(Resource):
#     def get(self):
#         return pprint.pformat (jira_api.projects())
