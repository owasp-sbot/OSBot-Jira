## Todo: refactor to a new OSBot_Slack (which also has the other classes currently in pbx_gs-python_utils
from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack

from osbot_jira.api.slack.blocks.Layout_Actions import Layout_Actions
from osbot_jira.api.slack.blocks.Layout_Context import Layout_Context
from osbot_jira.api.slack.blocks.Layout_Image import Layout_Image
from osbot_jira.api.slack.blocks.Layout_Section import Layout_Section


class API_Slack_Blocks:
    def __init__(self, text=None, callback_id=None, fallback=None):
        self.text            = text
        self.callback_id     = callback_id
        self.fallback        = fallback
        self.attachments     = []
        self.blocks          = []
        self.as_user         = False
        self.icon_emoji      = None
        self.icon_url        = None
        self.mrkdwn          = True
        self.link_names      = False
        self.parse           = 'none'
        self.username        = None
        self.kwargs          = None
        self.reply_broadcast = False
        self.thread_ts       = None
        self.unfurl_links    = False
        self.unfurl_media    = False
    # Helper methods

    def send_message(self,channel=None, team_id=None):                      # needs to move to the main dedicated lambda function
        api_slack = API_Slack(channel=channel, team_id=team_id)
        if  channel and team_id:                                            # to help with testing
            self.kwargs = {
                        'channel'        : api_slack.channel   ,
                        'text'           : self.text           ,
                        'as_user'        : self.as_user        ,
                        'attachments'    : self.attachments    ,
                        'blocks'         : self.blocks         ,
                        'icon_emoji'     : self.icon_emoji     ,
                        'icon_url'       : self.icon_url       ,
                        'link_names'     : self.link_names     ,
                        'mrkdwn'         : self.mrkdwn         ,
                        'parse'          : self.parse          ,
                        'reply_broadcast': self.reply_broadcast,
                        'thread_ts'      : self.thread_ts      ,
                        'unfurl_links'   : self.unfurl_links   ,
                        'unfurl_media'   : self.unfurl_media   ,
                        'username'       : self.username
                     }
            return api_slack.slack.api_call("chat.postMessage", **self.kwargs)
        else:
            return self.text, self.blocks

    def set_as_user        (self, value): self.as_user         = value ; return self
    def set_icon_emoji     (self, value): self.icon_emoji      = value ; return self
    def set_icon_url       (self, value): self.icon_url        = value ; return self
    def set_text           (self, value): self.text            = value ; return self
    def set_link_names     (self, value): self.link_names      = value ; return self
    def set_mrkdwn         (self, value): self.mrkdwn          = value ; return self
    def set_parse          (self, value): self.parse           = value ; return self
    def set_reply_broadcast(self, value): self.reply_broadcast = value ; return self
    def set_thread_ts      (self, value): self.thread_ts       = value ; return self
    def set_unfurl_links   (self, value): self.unfurl_links    = value ; return self
    def set_unfurl_media   (self, value): self.unfurl_media    = value ; return self
    def set_username       (self, value): self.username        = value ; return self

    # add layouts

    def add_layout_actions(self, block_id):
        return Layout_Actions(block_id, self.blocks)

    def add_layout_context(self, block_id):
        return Layout_Context(block_id, self.blocks)

    def add_layout_image(self, block_id, image_url, title=None, alt_text=None):
        return Layout_Image(block_id, self.blocks, image_url, title, alt_text)

    def add_layout_section(self, block_id):
        return Layout_Section(block_id, self.blocks)


    # add element blocks


    def add_divider(self):
        self.blocks.append({"type": "divider"})
        return self

    # def add_image(self, image_url, alt_text):
    #     self.blocks.append({ "type": "image", "image_url": image_url, "alt_text":  alt_text})

    def add_attachment(self,attachment):
        self.attachments.append(attachment)
        return self
    #def add_text
