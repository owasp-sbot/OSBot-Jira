## Todo: refactor to a new OSBot_Slack (which also has the other classes currently in pbx_gs-python_utils
from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack

class API_Slack_Blocks:
    def __init__(self, text=None, callback_id=None, fallback=None):
        self.text        = text
        self.callback_id = callback_id
        self.fallback    = fallback
        self.blocks      = []

    # Helper methods

    def send_message(self,channel=None, team_id=None):                      # needs to move to the main dedicated lambda function
        api_slack = API_Slack(channel=channel, team_id=team_id)
        if  channel and team_id:                                            # to help with testing
            return api_slack.slack.api_call("chat.postMessage", channel=api_slack.channel, text=self.text, blocks=self.blocks)
        else:
            return self.text, self.blocks

    def set_text(self, text):
        self.text = text
        return self

    # add blocks

    def add_divider(self):
        self.blocks.append({"type": "divider"})
        return self
