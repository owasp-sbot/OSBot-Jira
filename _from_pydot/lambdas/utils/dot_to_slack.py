import base64
import tempfile
import requests

from   pbx_gs_python_utils.utils.aws.secrets        import Secrets
from   pbx_gs_python_utils.utils.aws.Lambdas        import Lambdas


# def test_send_message(message):
#
#     channel_id = 'GBMGMK88Z'
#     result = send_message(channel_id, message)
#     return result

def upload_png_file(channel_id, file):
    bot_token = Secrets('slack-gs-bot').value()
    my_file = {
        'file': ('/tmp/myfile.pdf', open(file, 'rb'), 'png')
    }

    payload = {
        "filename"  : 'image.png',
        "token"     : bot_token,
        "channels"  : [channel_id],
    }
    requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    return 'image sent .... '


def run(event, context):
    channel         = event['channel']
    dot             = event['dot']

    (fd, tmp_file)  = tempfile.mkstemp('png)')
    dot_to_png      = Lambda('utils.dot_to_png').invoke
    png_data        = dot_to_png({"dot": dot, "width" : 500, "channel" : channel})


    if  len(png_data) > 5:
        with open(tmp_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))

        result = upload_png_file(channel, tmp_file)
        return result
    else:
        #slack_message(":red_circle: Error: could not create png file (file size: {0})".format(len(png_data)), [], channel)
        return { "status" : "error"}
