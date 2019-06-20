from pbx_gs_python_utils.utils import Misc
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message


class Slack_Jira_Search():

    def from_select_box(self,data):
        channel = data['channel']['id']
        team_id = data['team']['id']
        value   = data.get('value')

        slack_message('in Slack_Jira_Search.from_select_box: {0}'.format(value), [], channel, team_id)

        tmp = Misc.random_string_and_numbers()
        return  [
                {
                    "text": "Unexpected sentience: {0}".format(tmp),
                    "value": "AI-2323"
                },
                {
                    "text": "Bot biased toward other bots: {0}".format(data.get('value')),
                    "value": "SUPPORT-42"
                },
                {
                    "text": "Bot broke my toaster",
                    "value": "IOT-75"
                }
            ]


