import base64
import ssl

import certifi

from slack_sdk                  import WebClient

from osbot_utils.utils.Files import Files
from osbot_utils.utils.Misc import env_vars


class API_Slack:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        #client = slack.WebClient(token=os.environ['SLACK_TOKEN'], ssl=ssl_context)
        self.slack     = WebClient(self.bot_token,ssl=ssl_context)

    # def resolve_bot_token(self,use_env_vars):
    #     if use_env_vars:
    #         load_dotenv()
    #         self.slack_token = env_vars().get('SLACK_BOT_USER_TOKEN')
    #     else:
    #         pass  # add support for

    # todo: commented files need refactoring to new API

    def add_reaction(self, ts, reaction):
        return self.slack.reactions_add(channel =self.channel, name = reaction , timestamp=ts)
        #return self.slack.api_call( "reactions.add", channel =self.channel, name = reaction , timestamp=ts )

    # def team_logins(self, count = 100, pages = 1):
    #     logins = []
    #     for page in range(1,pages + 1):
    #         data  = self.slack.api_call('team.accessLogs', count = count, page = page)
    #         entries = data.get('logins')
    #         #print('[API Slack][team_logins] got {0} entries for page {1}'.format(len(entries), page))
    #         logins.extend(entries)
    #     return logins

    # def channels_history(self,channel):
    #     return self.slack.api_call("channels.history", channel = channel)

    #def channels_public(self):
    #     channels = {}
    #     cursor = None
    #     while cursor != '':
    #         data = self.slack.channels_list("channels.list", cursor=cursor)
    #         data = self.slack.api_call("channels.list", cursor = cursor)
    #         cursor = data.get('response_metadata').get('next_cursor')
    #         for channel in data['channels']:
    #             channels[channel['name']] = channel
    #     return channels

    # def channels_private(self):
    #     channels = {}
    #     for channel in self.slack.api_call("conversations.list", types='private_channel')['channels']:
    #         channels[channel['name']] = channel
    #     return channels

    # def delete_message(self,ts):
    #     return self.slack.api_call("chat.delete", channel=self.channel,ts=ts)

    def files_info(self, file_id):
        #files.info
        return self.slack.files_info(file=file_id).data

    def get_channel(self, channel):
        return self.slack.channels_info(channel=channel)

    # def get_messages(self,channel,limit=10):
    #     messages = self.slack.api_call("conversations.history", channel=channel, limit=limit).get('messages')
    #     return [message.get('text') for message in messages]

    def send_message(self, text, attachments = None, channel = None):
        if attachments is None:
            attachments = []
        if channel is None:
            channel = self.channel
        return self.slack.chat_postMessage(channel=channel,text=text, attachments=attachments).data
        # return self.slack.api_call("chat.postMessage",
        #                     channel     = channel,
        #                     text        = text ,
        #                     attachments = attachments)

    def set_channel(self, channel):
        self.channel = channel
        return self

    # at the moment this is using the REST API directly (see if there is a way to do this using the main Slack python API)

    def upload_file(self, file_path, channel, title=None):
        result = self.slack.files_upload(
            title    = title     ,
            file     = file_path ,
            channels = [channel]
        )
        return result.data

            #
            # import requests
            # file_name       = Files.file_name(file_path)
            # file_extension  = Files.file_extension(file_path)
            # if title is None: title = file_name
            # my_file        = {  'file': ('/tmp/file.png', open(file_path, 'rb'), file_extension) }
            #
            # payload        = {  "filename"  : '{0}.png'.format(title),
            #                     "token"     : self.bot_token        ,
            #                     "channels"  : [channel]              }
            # result = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
            # return result
            # return 'file sent to slack {0}'.format(file_path)

    def upload_image_from_png_base64(self, png_data, channel, title=None):
        png_file = Files.temp_file('.png')

        with open(png_file, "wb") as fh:
            fh.write(base64.decodebytes(png_data.encode()))
        return self.upload_file(png_file,channel,title)