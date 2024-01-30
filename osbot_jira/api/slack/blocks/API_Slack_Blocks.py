from osbot_jira.api.slack.API_Slack import API_Slack
from osbot_jira.api.slack.blocks.Layout_Actions import Layout_Actions
from osbot_jira.api.slack.blocks.Layout_Context import Layout_Context
from osbot_jira.api.slack.blocks.Layout_Image import Layout_Image
from osbot_jira.api.slack.blocks.Layout_Section import Layout_Section


class API_Slack_Blocks:
    def __init__(self, text=None, fallback=None):
        self.text            = text
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

    #NOT WORKING
    def send_message(self,channel=None, team_id=None):                      # needs to move to the main dedicated lambda function (since this version supports the Slack blocks feature)
        bot_token = ""      #todo: add support for bot token
        api_slack = API_Slack(bot_token)
        if  channel :                                            # to help with testing
            self.kwargs = {
                        #'channel'        : api_slack.channel   ,
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
            #return api_slack.slack.chat_postMessage(api_slack.channel, **self.kwargs)
            #return api_slack.slack.api_call("chat.postMessage", **self.kwargs)
            return api_slack.slack.chat_postMessage(channel=api_slack.channel, blocks=self.blocks).data
            #return api_slack.slack.chat_postMessage(channel=api_slack.channel,text=self.text, blocks=self.blocks)
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

    def add_layout_actions(self, action_id=None, block_id=None):
        return Layout_Actions(action_id, self.blocks,block_id)

    def add_layout_context(self, block_id=None):
        return Layout_Context(self.blocks,block_id)

    def add_layout_image(self, block_id, image_url, title=None, alt_text=None):
        return Layout_Image(block_id, self.blocks, image_url, title, alt_text)

    def add_layout_section(self, action_id=None, block_id=None):
        return Layout_Section(self.blocks, action_id, block_id)


    # add element blocks (which in most cases are simplified version of layout elements


    def add_divider(self):
        self.blocks.append({"type": "divider"})
        return self

    # def add_image(self, image_url, alt_text):
    #     self.blocks.append({ "type": "image", "image_url": image_url, "alt_text":  alt_text})

    def add_attachment(self,attachment):
        self.attachments.append(attachment)
        return self

    def add_text(self,text):
        return self.add_layout_section().add_text(text).render()

    def add_select(self,action_id, text, values):
        options = []
        for value in values:
                options.append((value, value))
        return self.add_layout_actions(action_id=action_id).add_select(text,options=options).render()

