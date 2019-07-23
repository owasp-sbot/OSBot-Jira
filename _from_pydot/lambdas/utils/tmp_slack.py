import ssl
import json
import base64
import urllib
from   utils.aws.secrets                         import Secrets

def send_message(channel_id, text, attachments=[]):
    bot_token = Secrets('slack-gs-bot').value()
    slack_url = "https://slack.com/api/chat.postMessage"

    data = urllib.parse.urlencode((("token", bot_token),  # oauth token
                                   ("channel", channel_id),  # channel to send message to
                                   ("text", text),  # message's text
                                   ("attachments", attachments)))  # message's attachments
    data = data.encode("ascii")
    request = urllib.request.Request(slack_url, data=data, method="POST")  # send data back to Slack
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    response = urllib.request.urlopen(request, context=context).read()

    return json.loads(response.decode())