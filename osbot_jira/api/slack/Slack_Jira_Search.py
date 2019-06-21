from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Misc import Misc
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

from osbot_jira.api.API_Issues import API_Issues


class Slack_Jira_Search():

    def from_select_box(self,data):

        if data.get('actions'):                                 # happens when the user selected an issue
            return self.handle_actions()

        return self.return_search_results(data.get('value'))    # happens when user types on dropdown

    def return_search_results(self,query):
        api_issues = API_Issues()
        issues = api_issues.search_using_lucene(query,15)
        results = { "options": [ ]}

        for issue in issues:
            text = "{1} - {0}".format(issue.get('Summary'), issue.get('Key'))
            results['options'].append({'text':text, 'value': issue.get('Key')})
        return results

    def handle_actions(self,data):
        channel = data['channel']['id']
        team_id = data['team']['id']
        actions = data.get('actions')
        issue_id = actions[0].get('selected_options')[0].get('value')
        payload = {'params': [issue_id], 'channel': channel, 'team_id': team_id}
        Lambda('osbot_jira.lambdas.elastic_jira').invoke_async(payload)
        return {"text": ":information_source: Issue selected: {0}".format(issue_id), "attachments": [],
                'replace_original': False}


    def get_drop_box_ui(self):
        text        = ''
        attachments = [{    "text": "Search jira",
                            "color": "#3AA3E3",
                            "attachment_type": "default",
                            "callback_id": "jira_search_select_box",
                            "actions": [
                                {
                                    # 'action_id': 'AAAAAAAAAA',
                                    "name": "query",
                                    "text": "query",
                                    "value": "",
                                    "type": "select",
                                    "data_source": "external",
                                    "min_query_length": 1,
                                }
                            ]
                        }]
        return text, attachments