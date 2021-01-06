from gw_bot.api.API_Slack import API_Slack
from osbot_aws.helpers.Lambda_Helpers import slack_message

from osbot_jira.api.slack.dialogs.Jira_Create_Issue import Jira_Create_Issue


class Slack_Message_Action:

    def __init__(self, message, trigger_id, channel=None, team_id=None):
        self.message    = message
        self.trigger_id = trigger_id
        self.channel    = channel
        self.team_id    = team_id

    def jira_create_issue_from_slack_message(self):
        if self.message:

            slack_message(':point_right: in jira_create_issue_from_slack_message')
            summary     = self.message.get('text')
            description = "{0}".format(self.message)
            if summary    : summary = summary.replace('+', ' ')
            if description: description = description.replace('+', ' ')
            slack_dialog = Jira_Create_Issue(summary=summary, description=description).setup().render()
            API_Slack(self.channel, self.team_id).slack.dialog_open(trigger_id=self.trigger_id, dialog=slack_dialog)
            return {"text": "in jira_create_issue_from_slack_message",  "attachments": [], 'replace_original': False}