from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Misc import Misc
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message

from osbot_jira.api.API_Issues import API_Issues
from osbot_jira.api.elk.Elk_To_Slack import ELK_to_Slack


class Slack_Jira_Search():

    def from_select_box(self,data):

        if data.get('actions'):                                 # happens when the user selected an issue
            return self.handle_actions(data)

        #channel = data['channel']['id']
        #team_id = data['team']['id']
        #slack_message('in handle actions for: {0}'.format(data), [], channel, team_id)

        return self.return_search_results(data.get('value'))    # happens when user types on dropdown

    def return_search_results(self,query):
        query = query.replace('+', ' ')
        max_show  = 100
        issues = ELK_to_Slack().cmd_search(query.split(' '))

        count = len(issues)
        options = []
        if count > max_show:
            options.append({'text':'[{0} matches, showing first {1}]'.format(count, max_show), 'value':'NA'})
        else:
            options.append({'text':'[{0} matches]'.format(count), 'value':'NA'})
        options.append({'text': '------------------------------', 'value':'NA'})

        issues = issues[0:max_show]
        items = {}
        for issue in issues:
           text = "{1}: {0}".format(issue.get('Summary'), issue.get('Issue Type'))
           items[text] = issue.get('Key')
        for text in sorted(items.keys()):
            options.append({'text': text, 'value': items[text]})

        return { "options": options}

    def handle_actions(self,data):
        channel = data['channel']['id']
        team_id = data['team']['id']
        actions = data.get('actions')

        issue_id = actions[0].get('selected_options')[0].get('value')
        payload = {'params': [issue_id], 'channel': channel, 'team_id': team_id}
        Lambda('osbot_jira.lambdas.elastic_jira').invoke_async(payload)
        return {"text": ":information_source: Issue selected: {0}".format(issue_id), "attachments": [], 'replace_original': False}


    def get_drop_box_ui(self):
        # dialog = API_Slack_Dialog()
        # dialog.add_element_select_external("Find issue", "key", "Search ELK for issue in indexes: jira and it_assets")
        # attachment = dialog.render()

        text        = ''
        attachments = [ {   "text": "Search jira (type to trigger search)",
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
                                    "min_query_length": 2,
                                }
                            ]
                        }]
        return text, attachments