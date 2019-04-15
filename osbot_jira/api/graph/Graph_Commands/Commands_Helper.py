import pprint

from pbx_gs_python_utils.utils.slack.API_Slack_Attachment import API_Slack_Attachment
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message, log_to_elk


class Commands_Helper():

    def __init__(self, target, with_slack_support=False):
        self.target             = target
        self.with_slack_support = with_slack_support

    def available_methods(self):
        return  [func for func in dir(self.target) if
                    callable(getattr(self.target, func)) and not func.startswith("_")]

    def help(self, prefix = ""):
        help_text = ""
        for command in self.available_methods():
            help_text += " • {0}\n".format(command)
        attachments = API_Slack_Attachment(help_text, 'good')
        text = prefix + "*Here are the `{0}` commands available:*".format(self.target.__name__)
        return text, attachments.render()

    def invoke(self, team_id, channel, params):
        attachments = []
        if len(params) == 0:
            (text, attachments) = self.help()
        else:
            command = params.pop(0)                                 # extract first element from the array
            if command in self.available_methods():
                method  = getattr(self.target, command)
                try:
                    if self.with_slack_support:
                        return method(team_id, channel, params)
                    else:
                        text, attachments = method(params)
                except Exception as error:
                    text = ':red_circle: Error processing params `{0}`: _{1}_'.format(params, pprint.pformat(error))
                    log_to_elk("Error in Lambda_Graph.handle_lambda_event :{0}".format(error), level='error')
            else:
                (text,attachments) = self.help(':red_circle: command not found `{0}`\n\n'.format(command))

        slack_message(text, attachments, channel, team_id)